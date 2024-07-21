import cv2
from ultralytics import YOLO
import glob
import time

# Load the YOLO model
model = YOLO("C:/Users/abdir/Desktop/models/best.pt")

# Define a glob search for all JPG files in a directory
image_paths = glob.glob("C:/Users/abdir/Desktop/_images/*.jpg")

# Desired FPS
desired_fps = 7.5
frame_duration = 1.0 / desired_fps

frame_count = 0
start_time = time.time()

for img_path in image_paths:
    frame_start_time = time.time()
    frame = cv2.imread(img_path)

    # Check if the image was successfully loaded
    if frame is not None:
        # Resize the frame to a quarter of its original size
        height, width = frame.shape[:2]
        frame = cv2.resize(frame, (width // 2, height // 2))

        # Run YOLO inference on the frame
        results = model(frame, conf=0.3)

        # FPS calculation
        frame_count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            fps = frame_count / elapsed_time
        else:
            fps = 0
        fps_display = f"FPS: {fps:.2f}"

        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        
        # Draw FPS on the annotated frame
        cv2.putText(annotated_frame, fps_display, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Display the annotated frame
        cv2.imshow("YOLO Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # Calculate and adjust to the desired frame rate
        time_used = time.time() - frame_start_time
        time_to_wait = frame_duration - time_used
        if time_to_wait > 0:
            time.sleep(time_to_wait)
    else:
        print(f"Failed to load image {img_path}")

# Close the display window
cv2.destroyAllWindows()
