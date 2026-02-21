import cv2

# ¶ÁÈ¡Í¼Ïñ
image = cv2.imread("captured_frame.jpg")  # Ìæ»»ÎªÄãµÄÍ¼Æ¬Â·¾¶

# ¼ì²éÍ¼ÏñÊÇ·ñ³É¹¦¼ÓÔØ
if image is None:
    print("Error: Could not read the image.")
else:
    # ÏÔÊ¾Í¼Ïñ
    cv2.imshow("Image Window", image)
    
    # µÈ´ý°´¼ü£¨0±íÊ¾ÎÞÏÞµÈ´ý£¬ÆäËûÊý×Ö±íÊ¾ºÁÃëÊý£©
    key = cv2.waitKey(0)
    
    # °´ÈÎÒâ¼ü¹Ø±Õ´°¿Ú£¨»òÖ¸¶¨°´¼ü£¬Èç°´ 'q' ÍË³ö£©
    if key == ord('q'):  # Èç¹û°´ÏÂ 'q' ¼ü
        cv2.destroyAllWindows()
