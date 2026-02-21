from ultralytics import YOLO

model = YOLO('./weights/yolov8n.pt')
model.export(format='onnx', dynamic=False, simplify=True, opset=12, batch=4,
             device=0, imgsz=(640, 640), nms=True)  #
