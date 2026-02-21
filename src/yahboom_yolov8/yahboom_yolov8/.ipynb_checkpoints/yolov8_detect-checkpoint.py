#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time
import sys
sys.path.append('/home/jetson/yahboomcar_ws/src/yahboom_yolov8/yahboom_yolov8/yolov8')
from ultralytics import YOLO
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

from cv_bridge import CvBridge
model = YOLO('/home/jetson/yahboomcar_ws/src/yahboom_yolov8/yahboom_yolov8/yolov8/weights/yolov8n.pt')



class Yolov8_Track(Node):
    def __init__(self,name):
        super().__init__(name)
        self.rgb_bridge = CvBridge()
        self.msg2img_bridge = CvBridge()
        self.yolov8_img_pub = self.create_publisher(Image,"detect_image",1)
        self.sub_rgb = self.create_subscription(Image,"/camera/color/image_raw",self.get_RGBImageCallBack,100)      

        
    def get_RGBImageCallBack(self,rgb_msg):
        rgb_image = self.msg2img_bridge.imgmsg_to_cv2(rgb_msg, "rgb8")
        self.process(rgb_image)


    def process(self,frame):
        results = model.track(frame, persist=True)
        print("----------------------------------------------------------------------")
        print("res: ",results[0])
        print("----------------------------------------------------------------------")
        annotated_frame = results[0].plot()
        ros_image = self.rgb_bridge.cv2_to_imgmsg(annotated_frame, encoding='rgb8')
        self.yolov8_img_pub.publish(ros_image)        
        

def main():
    rclpy.init()   
    yolov8_track = Yolov8_Track('yolov8_track_node')
    rclpy.spin(yolov8_track)	

if __name__ == '__main__':
	main()        
