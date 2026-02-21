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



def update_tracker(bboxes, image):
    bbox_xywh = []
    confs = []
    clss = []

    # 确保image是numpy数组格式
    if torch.is_tensor(image):
        image = image.cpu().numpy()
        image = image.transpose(1, 2, 0)
        image = (image * 255).astype(np.uint8)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 检查图像是否为空
    if image is None or image.size == 0:
        print("Error: Empty image passed to update_tracker")
        return []

    # 检查图像维度
    if len(image.shape) != 3:
        print(f"Error: Invalid image shape {image.shape}")
        return []

    for x1, y1, x2, y2, cls_id, conf in bboxes:
        obj = [
            int((x1+x2)/2), int((y1+y2)/2),
            max(1, x2-x1), max(1, y2-y1)  # 确保宽高至少为1
        ]
        bbox_xywh.append(obj)
        confs.append(conf)
        clss.append(cls_id)

    if not bbox_xywh:  # 如果没有检测到目标
        return []

    xywhs = torch.Tensor(bbox_xywh)
    confss = torch.Tensor(confs)

    # 添加调试信息
    print(f"Image shape: {image.shape}")
    print(f"Number of detections: {len(bbox_xywh)}")
    print(f"XYWH boxes: {bbox_xywh}")

    try:
        outputs = deepsort.update(xywhs, confss, clss, image)
    except Exception as e:
        print(f"DeepSort update error: {str(e)}")
        return []

    bboxes2draw = []
    current_ids = []
    for value in list(outputs):
        x1, y1, x2, y2, cls_, track_id = value
        bboxes2draw.append(
            (x1, y1, x2, y2, cls_, track_id)
        )
        current_ids.append(track_id)

    return bboxes2draw





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
        while cap.isOpened() and not stop:
            ret, frame = cap.read()
            if ret:
                # 保存原始帧
                original_frame = frame.copy()
                # 预处理帧
                frame_tensor, _, _, _ = preprocess(frame, imgsz=self.imgsz)
                img_list.append(frame_tensor)
                original_frames.append(original_frame)
                
                if len(img_list) == self.batch_size:
                    frames = torch.stack(img_list, 0)
                    t1 = time.perf_counter()
                    outputs = self.predict(frames)
                    t2 = time.perf_counter()
                    infer_time = (t2 - t1) / self.batch_size
                    outputs = non_max_suppression(outputs, 0.25, self.iou_thres, classes=None, agnostic=False)
                    
                    for i in range(self.batch_size):
                        t3 = time.perf_counter()
                        # 使用原始帧进行后处理
                        result = post_process(original_frames[i], outputs[i], frames)
                        t4 = time.perf_counter()
                        fps = 1 / (infer_time + t4 - t3)
                        cv2.putText(result, f"{fps:.2f} FPS", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        cv2.imshow("result", result)
                        if cv2.waitKey(1) & 0xFF == ord("q"):
                            stop = True
                            break
                    img_list = []
                    original_frames = []
            else:
                break
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
    # 在函数开始处添加转换
    if torch.is_tensor(frames):
        # 获取当前处理的帧
        frame = frames[0]  # 取出第一帧，因为frames是batch格式的
        frame = frame.cpu().numpy()  # 转换为numpy数组
        frame = frame.transpose(1, 2, 0)  # 调整维度顺序 (C,H,W) -> (H,W,C)
        frame = (frame * 255).astype(np.uint8)  # 恢复到0-255范围
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # 转换颜色空间
    else:
        frame = frames.copy()  # 创建副本以避免修改原始图像
    
    # 使用原始图像而不是处理后的frame
    processed_img = img.copy()
    
    bboxes = []
    if len(det):
        # 使用正确的输入shape进行边界框缩放
        det[:, :4] = scale_boxes((640, 640), det[:, :4], img.shape).round()
        
        for *xyxy, conf, cls in reversed(det):
            label = f'{names[int(cls)]} {conf:.2f}'
            score = conf.item()
            x1, y1, x2, y2 = map(int, xyxy)
            # 确保边界框坐标在有效范围内
            x1, x2 = max(0, x1), min(processed_img.shape[1], x2)
            y1, y2 = max(0, y1), min(processed_img.shape[0], y2)
            if x2 > x1 and y2 > y1:  # 只添加有效的边界框
                bboxes.append((x1, y1, x2, y2, float(cls), score))
        
        if bboxes:  # 只在有检测结果时调用tracker
            bboxes_tracker = update_tracker(bboxes, processed_img)
            
            for r in bboxes_tracker:
                x1, y1, x2, y2, class_id, track_id = r
                x1, x2 = int(x1), int(x2)
                y1, y2 = int(y1), int(y2)
                track_id = int(track_id)

                class_name = names[int(class_id)]
                distance_str = f"ID: {track_id}, {class_name}"
                text_size, _ = cv2.getTextSize(distance_str, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            
                center_x = (x1 + x2) // 2
                text_x = center_x - text_size[0] // 2
                text_y = max(y1 - 10, text_size[1])

                cv2.rectangle(processed_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(processed_img, distance_str, (text_x, text_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    
    return processed_img


if __name__ == '__main__':
    batch_size = 4
    trt_path = f"./weights/yolov8s.trt"
    trt_engine = TRT_engine(trt_path, batch_size=batch_size, thres=0.45, size=640, video_path="demo.mp4")
    trt_engine.process()
