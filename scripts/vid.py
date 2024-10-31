import cv2
from ultralytics import YOLO
import time

# Load the YOLOv8 model
model = YOLO("C:/Users/abdir/Desktop/models/best.pt")

# Open the video file
video_path = "C:/Users/abdir/"
cap = cv2.VideoCapture(video_path)

# Desired FPS
desired_fps = 7.5
frame_duration = 1.0 / desired_fps

frame_count = 0
start_time = time.time()

# Loop through the video frames
while cap.isOpened():
    frame_start_time = time.time()
    success, frame = cap.read()

    if success:
        # Resize the frame to a quarter of its original size
        height, width = frame.shape[:2]
        frame = cv2.resize(frame, (width // 2, height // 2))
        # Run YOLOv8 inference on the frame
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

        # Display the annotated frames
        cv2.imshow("Video Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        # Calculate and adjust to the desired frame rate
        time_used = time.time() - frame_start_time
        time_to_wait = frame_duration - time_used
        if time_to_wait > 0:
            time.sleep(time_to_wait)
    else:
        # Break the loop if the end of the video is reached
        break


# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
