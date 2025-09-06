from constants import classes, landing_statuses
from ultralytics import YOLO
import cv2
import glob
import time


model = YOLO("./yolov8m_640x640.pt")

image_paths = glob.glob("./_images/*.jpg")

# Desired FPS
desired_fps = 2.0
frame_duration = 1.0 / desired_fps

frame_count = 0
start_time = time.time()

for img_path in image_paths:
    frame_start_time = time.time()
    frame = cv2.imread(img_path)

    # Check if the image was successfully loaded
    if frame is not None:
        
        # Run YOLO inference on the frame
        results = model(frame, conf=0.3, imgsz=800, device=0)

        # FPS calculation
        frame_count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            fps = frame_count / elapsed_time
        else:
            fps = 0
        fps_display = f"FPS: {fps:.2f}"

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

        # Resize the frame to a quarter of its original size
        height, width = frame.shape[:2]
        resized_frame = cv2.resize(annotated_frame, (width // 2, height // 2))

        # Display FPS on the frame
        cv2.putText(resized_frame, fps_display, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv2.imshow("images Inference", resized_frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # calculate and adjust to the desired FPS
        time_used = time.time() - frame_start_time
        time_to_sleep = frame_duration - time_used
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

    else:
        print(f"Failed to load image {img_path}")

print(f"Frame count: {frame_count}")
cv2.destroyAllWindows()
