import cv2
import numpy as np
from collections import OrderedDict, namedtuple
import time
import torch
from ultralytics.utils.ops import non_max_suppression, scale_boxes
import tensorrt as trt


#############################
##deepscort

import numpy as np
import cv2
from imutils import resize
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import sys
import torchvision.transforms as transforms
from PIL import Image
import time
from tqdm import tqdm
from deep_sort.utils.parser import get_config
from deep_sort.deep_sort import DeepSort

#################################
#deepscort





palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)
cfg = get_config()
cfg.merge_from_file("deep_sort/configs/deep_sort.yaml")
deepsort = DeepSort(cfg.DEEPSORT.REID_CKPT,
                    max_dist=cfg.DEEPSORT.MAX_DIST, min_confidence=cfg.DEEPSORT.MIN_CONFIDENCE,
                    nms_max_overlap=cfg.DEEPSORT.NMS_MAX_OVERLAP, max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                    max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                    use_cuda=True)



def update_tracker(bboxes, image, skip_frames=200):
    """
    优化后的跟踪器更新函数
    """
    static_frame_count = 0
    
    if static_frame_count % skip_frames != 0:
        static_frame_count += 1
        return getattr(update_tracker, 'last_result', [])
    
    bbox_xywh = []
    confs = []
    clss = []

    # 优化图像格式转换
    if torch.is_tensor(image):
        image = image.cpu().numpy().transpose(1, 2, 0)
        image = (image * 255).astype(np.uint8)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if image is None or image.size == 0:
        return []

    # 使用列表推导式优化循环
    bbox_xywh = [(int((x1+x2)/2), int((y1+y2)/2), 
                  max(1, x2-x1), max(1, y2-y1)) 
                 for x1, y1, x2, y2, cls_id, conf in bboxes]
    
    if not bbox_xywh:
        return []

    try:
        # 修改：先在CPU上创建tensor，然后转移到GPU
        xywhs = torch.tensor(bbox_xywh, device='cpu')
        confss = torch.tensor([conf for *_, conf in bboxes], device='cpu')
        
        # 确保DeepSort接收CPU tensor
        outputs = deepsort.update(xywhs.cpu(), confss.cpu(), 
                                [cls_id for *_, cls_id, _ in bboxes], 
                                image)
        
        # 转换输出结果
        update_tracker.last_result = []
        for x1, y1, x2, y2, cls_, track_id in outputs:
            update_tracker.last_result.append((
                float(x1), float(y1), float(x2), float(y2),
                float(cls_), int(track_id)
            ))
        return update_tracker.last_result
    except Exception as e:
        print(f"DeepSort update error: {str(e)}")
        import traceback
        traceback.print_exc()  # 打印详细错误信息
        return []





####################################



names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
         'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
         'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
         'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
         'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
         'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
         'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
         'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
         'hair drier', 'toothbrush']  # coco80类别
colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in names]








def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=False, scaleup=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, r, (dw, dh)


class TRT_engine():
    def __init__(self, weight, thres=0.60, size=640, video_path='', batch_size=3) -> None:
        self.video_path = video_path
        self.imgsz = size
        self.weight = weight
        self.iou_thres = thres
        self.batch_size = batch_size
        self.device = torch.device('cuda:0')
        self.init_engine()

    def init_engine(self):
        # Infer TensorRT Engine
        self.Binding = namedtuple('Binding', ('name', 'dtype', 'shape', 'data', 'ptr'))
        self.logger = trt.Logger(trt.Logger.INFO)
        trt.init_libnvinfer_plugins(self.logger, namespace="")
        with open(self.weight, 'rb') as self.f, trt.Runtime(self.logger) as self.runtime:
            self.model = self.runtime.deserialize_cuda_engine(self.f.read())
        self.bindings = OrderedDict()
        print(f"num binding = {self.model.num_io_tensors}")
        for index in range(self.model.num_io_tensors):
            self.name = self.model.get_tensor_name(index)
            print(f"name = {self.name}")
            self.dtype = trt.nptype(self.model.get_tensor_dtype(self.name))
            self.shape = tuple(self.model.get_tensor_shape(self.name))
            print(f"shape = {self.shape}")  # 打印每个tensor的形状
            self.data = torch.from_numpy(np.empty(self.shape, dtype=np.dtype(self.dtype))).to(self.device)
            self.bindings[self.name] = self.Binding(self.name, self.dtype, self.shape, self.data,
                                                    int(self.data.data_ptr()))
        self.context = self.model.create_execution_context()
        # 设置输入和输出张量的地址
        for name, binding in self.bindings.items():
            self.context.set_tensor_address(name, binding.ptr)

    def predict(self, imgs):
        # 将输入数据复制到input tensor
        self.bindings['images'].data.copy_(imgs)
        
        # 执行推理
        self.context.execute_async_v3(torch.cuda.current_stream().cuda_stream)
        torch.cuda.synchronize()  # 等待推理完成

        outputs = self.bindings['output0'].data
        print(f"Output shape: {outputs.shape}")  # 打印输出tensor的形状
        print(f"Output sample: {outputs[0,:10]}")  # 打印部分输出数据
        return outputs

    def process(self):
        cap = cv2.VideoCapture(self.video_path)
        img_list = []
        original_frames = []
        stop = False
        
        # 设置更大的缓冲区
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        
        while cap.isOpened() and not stop:
            for _ in range(self.batch_size):
                ret, frame = cap.read()
                if not ret:
                    break
                
                # 移除分辨率缩放，使用原始分辨率
                original_frame = frame.copy()
                frame_tensor, _, _, _ = preprocess(frame, imgsz=self.imgsz)
                
                img_list.append(frame_tensor)
                original_frames.append(original_frame)
                
            if len(img_list) == 0:
                break
            
            if len(img_list) < self.batch_size:
                while len(img_list) < self.batch_size:
                    img_list.append(img_list[-1])
                    original_frames.append(original_frames[-1])
            
            # 批量处理并计时
            t1 = time.perf_counter()
            frames = torch.stack(img_list, 0)
            outputs = self.predict(frames)
            t2 = time.perf_counter()
            infer_time = (t2 - t1) / self.batch_size
            
            outputs = non_max_suppression(outputs, 0.25, self.iou_thres, classes=None, agnostic=False)
            
            for i in range(len(original_frames)):
                t3 = time.perf_counter()
                result = post_process(original_frames[i], outputs[i], frames)
                t4 = time.perf_counter()
                
                # 计算并显示FPS
                fps = 1 / (infer_time + (t4 - t3))
                cv2.putText(result, f"FPS: {fps:.1f}", (20, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.imshow("result", result)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    stop = True
                    break
                
            img_list = []
            original_frames = []
        cap.release()
        cv2.destroyAllWindows()


def preprocess(image, imgsz=640):
    img, ratio, (dw, dh) = letterbox(image, imgsz, stride=32, auto=False)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.transpose((2, 0, 1))
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(torch.device('cuda:0')).float()
    img /= 255.0
    return img, image, dw, dh


def post_process(img, det, frames):
    processed_img = img.copy()
    
    bboxes = []
    if len(det):
        det[:, :4] = scale_boxes((640, 640), det[:, :4], img.shape).round()
        
        for *xyxy, conf, cls in reversed(det):
            label = f'{names[int(cls)]} {conf:.2f}'
            x1, y1, x2, y2 = map(int, xyxy)
            x1, x2 = max(0, x1), min(processed_img.shape[1], x2)
            y1, y2 = max(0, y1), min(processed_img.shape[0], y2)
            
            if x2 > x1 and y2 > y1:
                bboxes.append((x1, y1, x2, y2, float(cls), conf.item()))
        
        if bboxes:
            bboxes_tracker = update_tracker(bboxes, processed_img)
            
            # 绘制跟踪框和ID
            for x1, y1, x2, y2, class_id, track_id in bboxes_tracker:
                x1, x2 = int(x1), int(x2)
                y1, y2 = int(y1), int(y2)
                track_id = int(track_id)
                
                # 获取类别名称
                class_name = names[int(class_id)]
                
                # 绘制边界框
                cv2.rectangle(processed_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # 绘制类别名称和跟踪ID
                label = f"{class_name}-{track_id}"
                t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                cv2.rectangle(processed_img, (x1, y1-t_size[1]-3), 
                            (x1+t_size[0], y1), (0, 255, 0), -1)
                cv2.putText(processed_img, label, (x1, y1-2), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    return processed_img


if __name__ == '__main__':
    batch_size = 4
    trt_path = f"./weights/yolov8s.trt"
    trt_engine = TRT_engine(trt_path, batch_size=batch_size, thres=0.45, size=640, video_path="demo.mp4")
    trt_engine.process()
