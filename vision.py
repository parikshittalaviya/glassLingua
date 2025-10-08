import cv2
import numpy as np
from tts_module import speak

def load_yolo():
    """Loads YOLO model for object detection."""
    weights_path = r"C:\Users\parik\Desktop\Glass Lingua\07_class_version\yolo3Requirements\yolov3.weights"
    config_path = r"C:\Users\parik\Desktop\Glass Lingua\07_class_version\yolo3Requirements\yolov3.cfg"
    labels_path = r"C:\Users\parik\Desktop\Glass Lingua\07_class_version\yolo3Requirements\coco.names"
    
    net = cv2.dnn.readNet(weights_path, config_path)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    
    with open(labels_path, "r") as f:
        classes = f.read().strip().split("\n")
    
    return net, output_layers, classes

def capture_image():
    """Captures an image from the webcam."""
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            speak("Failed to grab frame")
            break
        
        cv2.imshow("Press any key to capture (Press 'q' to e)", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return None  # Return None when 'q' is pressed to exit

        if key != 255:  # Any key other than 'q' is pressed
            image = frame.copy()
            cv2.imwrite(r"C:\Users\parik\Desktop\Glass Lingua\07_class_version\images\temp_images\temp.jpg", image)
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return image

def detect_book(image, net, output_layers):
    """Detects if a full book is present in the image using YOLO."""
    height, width, _ = image.shape
    blob = cv2.dnn.blobFromImage(image, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    
    class_ids, confidences, boxes = [], [], []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2 and class_id == 73:  # Class ID 73 for 'book'
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.3, nms_threshold=0.4)
    
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            margin = 10
            if x <= margin or y <= margin or (x + w) >= width - margin or (y + h) >= height - margin:
                print("Partial Book Detected")
                speak("Partial Book Detected.... Please try again")
                return None
            else:
                print("Full Book Detected")
                speak("Full Book Detected")
                return image
    else:
        print("No Book Detected")
        speak("No Book Detected... Please try again")
        return None
    
    