import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("C:/Users/w10/Downloads/runs/weights/best.pt")

# Open the video file
video_path = "C:/Users/w10/Downloads/2023 Örnek Video.mp4"
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Resize the frame to a quarter of its original size
        height, width = frame.shape[:2]
        frame = cv2.resize(frame, (width // 2, height // 2))
        # Run YOLOv8 inference on the frame
        results = model(frame, conf=0.25)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frames
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break


# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
