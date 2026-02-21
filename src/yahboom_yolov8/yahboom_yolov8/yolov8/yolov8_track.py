import cv2
from ultralytics import YOLO
import torch
from functools import partial

# ±£´æÔ­Ê¼µÄ torch.load
original_torch_load = torch.load

# Ê¹ÓÃ partial ¹Ì¶¨ weights_only=False
torch.load = partial(original_torch_load, weights_only=False)
print("11111111111111")

model = YOLO('./weights/yolov8n.pt')
print("2222222222222222222222")
# Open the video file
video_path = "./demo.mp4"
print(video_path)
cap = cv2.VideoCapture(video_path)
print("3333333333333333333333333333")
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        print("99999999999999999999")
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)
        print("---------------------------")
        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        print("***********************************")
        # Display the annotated frame
        #print(results[0].orig_img)
        #cv2.imshow("YOLOv8 Tracking", results[0].orig_img)
        print("66666666666666666666666666666666666")
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window	
cap.release()
cv2.destroyAllWindows()
