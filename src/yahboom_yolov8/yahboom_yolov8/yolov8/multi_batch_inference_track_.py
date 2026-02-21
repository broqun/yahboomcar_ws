import cv2
import numpy as np
from collections import OrderedDict, namedtuple
import time
import torch
from ultralytics.utils.ops import non_max_suppression, scale_boxes
import tensorrt as trt
import threading
from queue import Queue
import torch.multiprocessing as mp


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
deepsort = DeepSort(
    cfg.DEEPSORT.REID_CKPT,
    max_dist=0.15,           # 进一步降低最大距离阈值，提高匹配精度
    min_confidence=0.25,     # 降低最小置信度，避免漏检
    nms_max_overlap=0.8,     # 提高NMS阈值，保留更多重叠框
    max_iou_distance=0.5,    # 降低IOU距离阈值，提高匹配精度
    max_age=50,             # 增加存活帧数，提高跟踪稳定性
    n_init=2,               # 减少初始化帧数，加快目标确认
    nn_budget=150,          # 增加特征库大小
    use_cuda=True
)



def process_roi(bboxes, roi_image):
    """处理ROI区域的跟踪"""
    try:
        # 检查ROI图像是否有效
        if roi_image is None or roi_image.size == 0 or roi_image.shape[0] == 0 or roi_image.shape[1] == 0:
            print(f"Invalid ROI image shape: {roi_image.shape if roi_image is not None else None}")
            return []
            
        bbox_xywh = [(int((x1+x2)/2), int((y1+y2)/2), 
                      max(1, x2-x1), max(1, y2-y1)) 
                     for x1, y1, x2, y2, *_ in bboxes]
        
        if not bbox_xywh:
            return []
            
        xywhs = torch.tensor(bbox_xywh, device='cpu')
        confss = torch.tensor([conf for *_, conf in bboxes], device='cpu')
        clss = [cls_id for *_, cls_id, _ in bboxes]
        
        outputs = deepsort.update(xywhs.cpu(), confss.cpu(), clss, roi_image)
        return outputs
    except Exception as e:
        print(f"Process ROI error: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def update_tracker(bboxes, image, skip_frames=150):  # 减少跳帧数以提高准确率
    static_frame_count = 0
    
    if static_frame_count % skip_frames != 0:
        static_frame_count += 1
        return getattr(update_tracker, 'last_result', [])
    
    if bboxes and image is not None:
        try:
            # 降低过滤阈值，保留更多目标
            MIN_CONF = 0.25  # 降低最小置信度
            MIN_BOX_AREA = 100  # 降低最小目标面积
            
            # 过滤低质量目标
            filtered_bboxes = []
            for x1, y1, x2, y2, cls_id, conf in bboxes:
                area = (x2 - x1) * (y2 - y1)
                if area > MIN_BOX_AREA and conf > MIN_CONF:
                    filtered_bboxes.append((x1, y1, x2, y2, cls_id, conf))
            
            if not filtered_bboxes:
                return []
                
            # 增大ROI区域
            margin = min(150, min(image.shape[0], image.shape[1]) // 6)  # 增加margin
            x_min = max(0, int(min(x1 for x1, *_ in filtered_bboxes)) - margin)
            y_min = max(0, int(min(y1 for _, y1, *_ in filtered_bboxes)) - margin)
            x_max = min(image.shape[1], int(max(x2 for *_, x2, _, _ in filtered_bboxes)) + margin)
            y_max = min(image.shape[0], int(max(y2 for *_, _, y2, _, _ in filtered_bboxes)) + margin)
            
            # 确保ROI区域有效
            if x_max <= x_min or y_max <= y_min:
                return []
            
            # 提取ROI区域
            roi_image = image[y_min:y_max, x_min:x_max].copy()
            
            # 检查ROI是否有效
            if roi_image is None or roi_image.size == 0:
                return []
            
            # 调整边界框坐标
            adjusted_bboxes = []
            for x1, y1, x2, y2, cls_id, conf in filtered_bboxes:
                # 确保坐标在有效范围内
                adj_x1 = max(0, x1 - x_min)
                adj_y1 = max(0, y1 - y_min)
                adj_x2 = min(x_max - x_min, x2 - x_min)
                adj_y2 = min(y_max - y_min, y2 - y_min)
                
                if adj_x2 > adj_x1 and adj_y2 > adj_y1:
                    adjusted_bboxes.append((
                        adj_x1, adj_y1, adj_x2, adj_y2,
                        cls_id, conf
                    ))
            
            if not adjusted_bboxes:
                return []
            
            # 在ROI上运行DeepSort
            results = process_roi(adjusted_bboxes, roi_image)
            
            # 还原坐标
            final_results = []
            for x1, y1, x2, y2, cls_, track_id in results:
                final_results.append((
                    x1 + x_min, y1 + y_min,
                    x2 + x_min, y2 + y_min,
                    cls_, track_id
                ))
            return final_results
            
        except Exception as e:
            print(f"ROI processing error: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
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


class VideoProcessor:
    def __init__(self, max_size=30):
        self.frame_queue = Queue(maxsize=max_size)
        self.result_queue = Queue(maxsize=max_size)
        self.running = False
        
    def start(self):
        self.running = True
        self.capture_thread = threading.Thread(target=self.capture_frames)
        self.process_thread = threading.Thread(target=self.process_frames)
        self.display_thread = threading.Thread(target=self.display_frames)
        self.capture_thread.start()
        self.process_thread.start()
        self.display_thread.start()


class TRT_engine():
    def __init__(self, weight, thres=0.60, size=640, video_path='', batch_size=3):
        self.video_path = video_path
        self.imgsz = size
        self.weight = weight
        self.iou_thres = thres
        self.batch_size = batch_size
        self.device = torch.device('cuda:0')
        self.init_engine()
        self.processor = VideoProcessor()
        
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

    def preprocess_cuda(self, image):
        """使用GPU加速图像预处理"""
        # 首先调整图像大小到目标尺寸
        img, ratio, (dw, dh) = letterbox(image, self.imgsz, stride=32, auto=False)
        
        # 转换为RGB并移动到GPU
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = torch.from_numpy(img).cuda().float()
        img = img.permute(2, 0, 1).unsqueeze(0)  # HWC to BCHW
        img /= 255.0  # 归一化到0-1
        
        return img, ratio, (dw, dh)

    def process(self):
        cap = cv2.VideoCapture(self.video_path)
        
        # 设置缓冲区
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 30)
        
        frame_count = 0
        PROCESS_EVERY_N_FRAMES = 3  # 跳帧数
        
        while cap.isOpened():
            frame_count += 1
            if frame_count % PROCESS_EVERY_N_FRAMES != 0:
                cap.grab()
                continue
                
            frames_batch = []
            original_frames = []
            ratios = []
            pads = []
            
            # 批量读取帧
            for _ in range(self.batch_size):
                ret, frame = cap.read()
                if not ret:
                    break
                
                # 预处理
                frame_tensor, ratio, pad = self.preprocess_cuda(frame)
                frames_batch.append(frame_tensor)
                original_frames.append(frame)
                ratios.append(ratio)
                pads.append(pad)
            
            if not frames_batch:
                break
            
            # 堆叠批次
            try:
                frames = torch.cat(frames_batch, 0)  # 将批次维度堆叠
                
                # 执行推理
                t1 = time.perf_counter()
                outputs = self.predict(frames)
                t2 = time.perf_counter()
                outputs = non_max_suppression(outputs, 
                                    conf_thres=0.25,  # 降低置信度阈值
                                    iou_thres=0.6,    # 调整IOU阈值
                                    classes=None,      # 保留所有类别
                                    agnostic=True)     # 使用类别无关的NMS
                
                # 处理每一帧的结果
                for i, (output, orig_img, ratio, pad) in enumerate(zip(outputs, original_frames, ratios, pads)):
                    t3 = time.perf_counter()
                    # 缩放检测框到原始图像尺寸
                    if output is not None:
                        output[:, :4] = scale_boxes((self.imgsz, self.imgsz), 
                                                  output[:, :4], 
                                                  orig_img.shape).round()
                    
                    result = self.post_process_cuda(orig_img, output, frames)
                    t4 = time.perf_counter()
                    
                    # 计算FPS
                    fps = 1.0 / ((t2 - t1) / self.batch_size + (t4 - t3))
                    cv2.putText(result, f'FPS: {fps:.1f}', (20, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    cv2.imshow('result', result)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        cap.release()
                        cv2.destroyAllWindows()
                        return
                    
            except Exception as e:
                print(f"Processing error: {str(e)}")
                continue
            
            frames_batch = []
            original_frames = []
            ratios = []
            pads = []
        
        cap.release()
        cv2.destroyAllWindows()

    def predict(self, imgs):
        """执行TensorRT推理"""
        try:
            # 确保输入数据形状正确
            if imgs.shape[2:] != (self.imgsz, self.imgsz):
                raise ValueError(f"Input shape {imgs.shape} does not match expected shape {(self.batch_size, 3, self.imgsz, self.imgsz)}")
            
            # 复制数据到input tensor
            self.bindings['images'].data.copy_(imgs)
            
            # 执行推理
            self.context.execute_async_v3(torch.cuda.current_stream().cuda_stream)
            torch.cuda.synchronize()
            
            return self.bindings['output0'].data
            
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return None

    def post_process_cuda(self, img, det, frames):
        processed_img = img.copy()
        
        bboxes = []
        if det is not None and len(det):
            for *xyxy, conf, cls in det:
                try:
                    x1, y1, x2, y2 = map(int, [float(x) for x in xyxy])
                    
                    # 放宽边界框的有效性检查
                    if x2 <= x1 or y2 <= y1:
                        continue
                        
                    # 降低最小目标大小限制
                    width = x2 - x1
                    height = y2 - y1
                    if width < 5 or height < 5:  # 降低最小尺寸阈值
                        continue
                    
                    # 确保坐标在图像范围内
                    x1 = max(0, min(x1, processed_img.shape[1] - 1))
                    x2 = max(0, min(x2, processed_img.shape[1] - 1))
                    y1 = max(0, min(y1, processed_img.shape[0] - 1))
                    y2 = max(0, min(y2, processed_img.shape[0] - 1))
                    
                    # 降低置信度阈值
                    if x2 > x1 and y2 > y1 and float(conf) > 0.25:  # 降低置信度阈值
                        bboxes.append((x1, y1, x2, y2, float(cls), float(conf)))
                except Exception as e:
                    continue
            
            if bboxes:
                # 更新跟踪器
                bboxes_tracker = update_tracker(bboxes, processed_img)
                
                if bboxes_tracker:
                    # 添加轨迹显示
                    tracks_dict = {}  # 用于存储轨迹
                    for x1, y1, x2, y2, class_id, track_id in bboxes_tracker:
                        try:
                            # 计算目标中心点
                            center = (int((x1 + x2) / 2), int((y1 + y2) / 2))
                            
                            # 更新轨迹
                            if track_id not in tracks_dict:
                                tracks_dict[track_id] = []
                            tracks_dict[track_id].append(center)
                            
                            # 限制轨迹长度
                            if len(tracks_dict[track_id]) > 30:  # 保持最近30帧的轨迹
                                tracks_dict[track_id] = tracks_dict[track_id][-30:]
                            
                            # 绘制轨迹
                            if len(tracks_dict[track_id]) > 1:
                                points = np.array(tracks_dict[track_id], np.int32)
                                cv2.polylines(processed_img, [points],
                                            False, colors[int(class_id) % len(colors)], 2)
                            
                            # 获取该类别的颜色
                            color = colors[int(class_id) % len(colors)]
                            
                            # 绘制边界框
                            cv2.rectangle(processed_img, 
                                        (x1, y1), (x2, y2),
                                        color, 2)
                            
                            # 准备标签文本
                            label = f"{names[int(class_id)]}-{track_id}"
                            
                            # 获取文本大小
                            t_size = cv2.getTextSize(label, 
                                                   cv2.FONT_HERSHEY_SIMPLEX,
                                                   0.6, 2)[0]
                            
                            # 绘制标签背景
                            cv2.rectangle(processed_img, 
                                        (x1, y1 - t_size[1] - 3),
                                        (x1 + t_size[0], y1), 
                                        color, -1)
                            
                            # 绘制标签文本
                            cv2.putText(processed_img, label,
                                      (x1, y1 - 2),
                                      cv2.FONT_HERSHEY_SIMPLEX,
                                      0.6, (255, 255, 255), 2)
                            
                        except Exception as e:
                            continue
        
        return processed_img


if __name__ == '__main__':
    batch_size = 4
    trt_path = f"./weights/yolov8s.trt"
    trt_engine = TRT_engine(trt_path, batch_size=batch_size, thres=0.45, size=640, video_path="demo.mp4")
    trt_engine.process()
