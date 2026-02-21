import cv2
import numpy as np
from collections import OrderedDict, namedtuple
import time
import torch
from ultralytics.utils.ops import non_max_suppression, scale_boxes
import tensorrt as trt

names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
         'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
         'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
         'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
         'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
         'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
         'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
         'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
         'hair drier', 'toothbrush']
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
                        print("-----------------------------------------")
                        cv2.putText(result, f"{fps:.2f} FPS", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        print("++++++++++++++++++++++++++++++++++++++")
                        cv2.imwrite("captured_frame.jpg", result)

                        #cv2.imshow("result", result)
                        #cv2.waitKey(0)
                        print("`````````````````````````````````````````````````````````````")
                        
                        '''if cv2.waitKey(1) & 0xFF == ord("q"):
                            stop = True
                            break'''
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
    processed_img = img.copy()
    
    if len(det):
        det[:, :4] = scale_boxes((640, 640), det[:, :4], img.shape).round()
        
        for *xyxy, conf, cls in reversed(det):
            c = int(cls)
            label = f'{names[c]} {conf:.2f}'
            x1, y1, x2, y2 = map(int, xyxy)
            
            # 确保边界框坐标在有效范围内
            x1, x2 = max(0, x1), min(processed_img.shape[1], x2)
            y1, y2 = max(0, y1), min(processed_img.shape[0], y2)
            
            if x2 > x1 and y2 > y1:  # 只绘制有效的边界框
                color = colors[c]
                cv2.rectangle(processed_img, (x1, y1), (x2, y2), color, 2)
                # 添加标签背景
                text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                cv2.rectangle(processed_img, (x1, y1 - text_size[1] - 4), (x1 + text_size[0], y1), color, -1)
                # 添加白色文本
                cv2.putText(processed_img, label, (x1, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    return processed_img

if __name__ == '__main__':
    batch_size = 4
    trt_path = f"./weights/yolov8s.trt"
    trt_engine = TRT_engine(trt_path, batch_size=batch_size, thres=0.45, size=640, video_path="demo.mp4")
    trt_engine.process()
