from constants import classes, landing_statuses
#from .detected_object import DetectedObject
from ultralytics import YOLO
import cv2
import glob


model = YOLO("C:/Users/abdir/Desktop/models/best.pt")

image_paths = glob.glob("C:/Users/abdir/Desktop/_images/*.jpg")

for img_path in image_paths:
    frame = cv2.imread(img_path)

    # Check if the image was successfully loaded
    if frame is not None:
        # Resize the frame to a quarter of its original size
        height, width = frame.shape[:2]
        frame = cv2.resize(frame, (width // 2, height // 2))

        # Run YOLO inference on the frame
        results = model(frame, conf=0.3, imgsz=800)

        detected_boxes = results[0].boxes

        vehicles = []
        humans = []
        fcp_areas = []
        fal_areas = []

        # Categorize detected objects
        for box in detected_boxes:
            cls = int(box.cls[0])
            x0, y0, x1, y1 = map(int, box.xyxy[0])

            if cls == 0:
                vehicles.append([x0, y0, x1, y1, cls])
            elif cls == 1:
                humans.append([x0, y0, x1, y1, cls])
            elif cls == 2:
                fcp_areas.append([x0, y0, x1, y1, cls])
            elif cls == 3:
                fal_areas.append([x0, y0, x1, y1, cls])

        # Check overlaps and determine landing status
        for area in fcp_areas + fal_areas:
            x0, y0, x1, y1, cls = area
            area_suitable = True

            for obj in vehicles + humans:
                obj_x0, obj_y0, obj_x1, obj_y1, obj_cls = obj
                if obj_x0 < x1 and obj_x1 > x0 and obj_y0 < y1 and obj_y1 > y0:
                    area_suitable = False
                    break

            landing_status = landing_statuses["Inilebilir"] if area_suitable else landing_statuses["Inilemez"]
            
            # Print DetectedObject information
            print(f"DetectedObject(cls={cls}, landing_status={landing_status}, "
                f"top_left_x={x0}, top_left_y={y0}, bottom_right_x={x1}, bottom_right_y={y1})")

        # Create DetectedObject instances for vehicles
        for obj in vehicles:
            obj_x0, obj_y0, obj_x1, obj_y1, obj_cls = obj
            print(f"DetectedObject(cls={obj_cls}, landing_status={landing_statuses['Inis Alani Degil']}, "
                f"top_left_x={obj_x0}, top_left_y={obj_y0}, bottom_right_x={obj_x1}, bottom_right_y={obj_y1})")

        # Create DetectedObject instances for humans
        for obj in humans:
            obj_x0, obj_y0, obj_x1, obj_y1, obj_cls = obj
            print(f"DetectedObject(cls={obj_cls}, landing_status={landing_statuses['Inis Alani Degil']}, "
                f"top_left_x={obj_x0}, top_left_y={obj_y0}, bottom_right_x={obj_x1}, bottom_right_y={obj_y1})")
            
        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        
        cv2.imshow("images Inference", annotated_frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        print(f"Failed to load image {img_path}")

# Close the display window
cv2.destroyAllWindows()