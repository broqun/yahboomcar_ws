#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from collections import OrderedDict, namedtuple
import time
import torch
import sys
sys.path.append('/home/jetson/yahboomcar_ws/src/yahboom_yolov8/yahboom_yolov8/yolov8')
import tracker_trt
from ultralytics.utils.ops import non_max_suppression, scale_boxes
import tensorrt as trt
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Int16
from cv_bridge import CvBridge
from yahboom_yolov8.Robot_Move import *
from yahboom_yolov8.common import *
from geometry_msgs.msg import Twist
from arm_msgs.msg import ArmJoints
from sensor_msgs.msg import LaserScan
import math
import os
RAD2DEG = 180 / math.pi
encoding = ['16UC1', '32FC1']

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


print("--------------------------------------------")

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

class TRT_engine(Node):
    def __init__(self, weight, thres=0.60, size=640, video_path='', batch_size=3) -> None:
        super().__init__('yolov8_node')  # ½ÚµãÃû³Æ
        self.video_path = video_path
        self.imgsz = size
        self.weight = weight
        self.iou_thres = thres
        self.batch_size = batch_size
        self.device = torch.device('cuda:0')
        self.init_engine()
        self.frame = None
        self.rgb_bridge = CvBridge()
        self.msg2img_bridge = CvBridge()
        self.TargetAngle_pub = self.create_publisher(ArmJoints, "arm6_joints", 10)
        self.yolov8_img_pub = self.create_publisher(Image,"detect_image",1)
        self.cmd_pub = self.create_publisher(Twist,"/cmd_vel",1)
        self.sub_rgb = self.create_subscription(Image,"/camera/color/image_raw",self.get_RGBImageCallBack,1)
        self.sub_laser = self.create_subscription(LaserScan,"/scan",self.registerScan,1)
        self.trackered_id = None
        self.sub_t_id = self.create_subscription(Int16,"/tracker_id",self.get_IDCallBack,100)
        self.vel = Twist()
        self.angular_PID = (0.5, 0.0, 0.3)
        self.lin_pid = SinglePID(0.5, 0.0, 0.1)
        self.angular_pid = simplePID(self.angular_PID[0] / 100.0, self.angular_PID[1] / 100.0, self.angular_PID[2] / 100.0)
        self.found = False
        self.joy_ctrl = False
        self.init_joints = [90, 178, 0, 0, 90, 90]
        while not self.TargetAngle_pub.get_subscription_count():
        	self.pubSix_Arm(self.init_joints)
        	time.sleep(0.1)	
        self.pubSix_Arm(self.init_joints)  
        self.img_list = []
        self.original_frames = []  
        self.LaserAngle = 5
        self.depth_image_info = []
        self.depth_bridge = CvBridge()
        self.rotation_done = False
        self.ResponseDist = 1.2

    def exit_pro(self):
        cmd1 = "ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "
        cmd2 = '''"{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"'''
        cmd = cmd1 +cmd2
        os.system(cmd)

        

    def registerScan(self, scan_data):
        if not isinstance(scan_data, LaserScan): return
        ranges = np.array(scan_data.ranges)
        minDistList = []
        minDistIDList = []
        for i in range(len(ranges)):
            angle = (scan_data.angle_min + scan_data.angle_increment * i) * RAD2DEG
            if abs(angle) < self.LaserAngle and ranges[i] !=0.0 : 
            	minDistList.append(ranges[i])
            	minDistIDList.append(angle)
        if len(minDistList) == 0: return
        minDist = min(minDistList)
        minDistID = minDistIDList[minDistList.index(minDist)]
        #print("minDistID: ",minDistID)
        print("minDist: ",minDist)
        if self.rotation_done == True:
            if abs(minDist - self.ResponseDist) < 0.2:
                minDist = self.ResponseDist
                self.cmd_pub.publish(Twist())
            else:
                #print("Adjust dist.")
                if not math.isinf(minDist): 
                    linear_x = -self.lin_pid.pid_compute(self.ResponseDist, minDist)
                    print("linear_x: ",linear_x)                   
                    self.vel.linear.x = linear_x
                    self.cmd_pub.publish(self.vel)


		
    def pubSix_Arm(self, joints, id=6, angle=180.0, runtime=2000):
        arm_joint =ArmJoints()
        arm_joint.joint1 = joints[0]
        arm_joint.joint2 = joints[1]
        arm_joint.joint3 = joints[2]
        arm_joint.joint4 = joints[3]
        arm_joint.joint5 = joints[4]
        arm_joint.joint6 = joints[5]
        arm_joint.time = runtime
        self.TargetAngle_pub.publish(arm_joint)
        
        
    def get_IDCallBack(self,msg):
        self.trackered_id = msg.data

    def get_RGBImageCallBack(self,rgb_msg):
        self.frame = rgb_msg
        self.process()
        
    
    def init_engine(self):
        # Infer TensorRT Engine
        self.Binding = namedtuple('Binding', ('name', 'dtype', 'shape', 'data', 'ptr'))
        self.logger = trt.Logger(trt.Logger.INFO)
        trt.init_libnvinfer_plugins(self.logger, namespace="")
        with open(self.weight, 'rb') as self.f, trt.Runtime(self.logger) as self.runtime:
            self.model = self.runtime.deserialize_cuda_engine(self.f.read())
            
        self.bindings = OrderedDict()

        for index in range(self.model.num_io_tensors):
            self.name = self.model.get_tensor_name(index)

            self.dtype = trt.nptype(self.model.get_tensor_dtype(self.name))
            self.shape = tuple(self.model.get_tensor_shape(self.name))
            self.data = torch.from_numpy(np.empty(self.shape, dtype=np.dtype(self.dtype))).to(self.device)
            self.bindings[self.name] = self.Binding(self.name, self.dtype, self.shape, self.data,
                                                   int(self.data.data_ptr()))
        self.context_ = self.model.create_execution_context()
        # 设置输入和输出张量的地址
        for name, binding in self.bindings.items():
            self.context_.set_tensor_address(name, binding.ptr)

    def predict(self, imgs):
        # 将输入数据复制到input tensor
        self.bindings['images'].data.copy_(imgs)
        
        # 执行推理
        self.context_.execute_async_v3(torch.cuda.current_stream().cuda_stream)
        torch.cuda.synchronize()  # 等待推理完成

        outputs = self.bindings['output0'].data
        #print(f"Output shape: {outputs.shape}")  # 打印输出tensor的形状
        #print(f"Output sample: {outputs[0,:10]}")  # 打印部分输出数据
        return outputs

    def process(self):
     
        frame = self.msg2img_bridge.imgmsg_to_cv2(self.frame, "rgb8")
        #original_frame = frame.copy()
        # 预处理帧
        frame_tensor, _, dw, dh = preprocess(frame, imgsz=self.imgsz)
        self.img_list.append(frame_tensor)
        self.original_frames.append(frame)   
        #print(len(self.img_list))
        if len(self.img_list) == self.batch_size:
            frames = torch.stack(self.img_list, 0)
            t1 = time.perf_counter()
            outputs = self.predict(frames)
            t2 = time.perf_counter()
            infer_time = (t2 - t1) / self.batch_size
            outputs = non_max_suppression(outputs, 0.25, self.iou_thres, classes=None, agnostic=False)
            
            for i in range(self.batch_size):
                t3 = time.perf_counter()
                # 使用原始帧进行后处理
                result,det_infos = post_process(self.original_frames[i], outputs[i], frames)
                
                list_bbox = tracker_trt.update(det_infos,frame)
                for (x1, y1, x2, y2, cls, track_id) in list_bbox:
                    color = [0, 255, 0]
                    cv2.rectangle(result, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                    cv2.putText(result, f'{cls} {track_id}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    if  track_id == self.trackered_id:
                        self.found = True
                        color = [0, 0, 255]
                        self.cx = (x1 + x2)/2
                        self.cy = (y1 + y2)/2
                        cv2.circle(result, (int(self.cx), int(self.cy)), 5, (255, 255, 0), 2)
                        cv2.rectangle(result, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                        cv2.putText(result, f'{cls} {track_id}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                        
                        
                t4 = time.perf_counter()
                fps = 1 / (infer_time + t4 - t3)
                cv2.putText(result, f"{fps:.2f} FPS", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2) 
                ros_image = self.rgb_bridge.cv2_to_imgmsg(result, encoding='rgb8')
                self.yolov8_img_pub.publish(ros_image)
            if self.found == True and self.joy_ctrl == False:
                if abs(self.cx - 320 )>5:
                    angular_z = self.angular_pid.compute(320, self.cx)
                    if abs(angular_z) < 0.1:
                        angular_z = 0.0 
                        self.rotation_done = True
                        self.vel.angular.z = angular_z
                        self.cmd_pub.publish(self.vel)
                    else:
                        self.rotation_done = False
                        print("angular_z: ",angular_z)
                        self.vel.angular.z = angular_z
                        self.cmd_pub.publish(self.vel) 
                else:
                    self.cmd_pub.publish(Twist())
            else:
                self.cmd_pub.publish(Twist())
            self.img_list = []
            self.original_frames = []
            self.found = False          
        '''else:
            stop = Twist()      
            self.cmd_pub.publish(stop)  '''

def preprocess(image, imgsz=640):
    img, ratio, (dw, dh) = letterbox(image, imgsz, stride=32, auto=False)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.transpose((2, 0, 1))
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(torch.device('cuda:0')).float()
    img /= 255.0
    return img, image, dw, dh

def post_process(img, det, frames):
    """
    Draw bounding boxes on the input image.
    """
    detections = []
    if len(det):
        # Rescale boxes from img_size to im0 size
        det[:, :4] = scale_boxes(frames.shape[2:], det[:, :4], img.shape).round()
        for *xyxy, conf, cls in reversed(det):
            label = f'{names[int(cls)]} {conf:.2f}'
            cls_id = int(cls)
            cls1 = names[int(cls)]

            detections.append((int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3]), cls1, conf.item()))
    return img, detections


    
def main():
    rclpy.init()   
    batch_size = 1
    trt_path = f"/home/jetson/yahboomcar_ws/src/yahboom_yolov8/yahboom_yolov8/yolov8/weights/yolov8s.trt"
    trt_engine = TRT_engine(trt_path, batch_size=batch_size, thres=0.45, size=640, video_path="/home/jetson/yahboomcar_ws/src/yahboom_yolov8/yahboom_yolov8/yolov8/demo.mp4")
    try:
        rclpy.spin(trt_engine)
    except KeyboardInterrupt:
        pass
    finally:
        trt_engine.exit_pro()
        trt_engine.destroy_node()
        rclpy.shutdown()    
    #trt_engine.process()	

if __name__ == '__main__':
	main()

