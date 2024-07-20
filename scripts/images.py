import cv2
from ultralytics import YOLO
import glob

# Load the YOLOv8 model
model = YOLO(
    "C:/Users/w10/Desktop/Python-env/first_train/runs/detect/train/weights/best.pt"
)

# Define a glob search for all JPG files in a directory
image_paths = glob.glob(
    "C:/Users/w10/Desktop/Python-env/first_train/Dataset/images/val/*.jpg"
)

# Loop through the image paths
for img_path in image_paths:
    # Read the image
    frame = cv2.imread(img_path)

    # Check if the image was successfully loaded
    if frame is not None:
        # Resize the frame to a quarter of its original size
        height, width = frame.shape[:2]
        frame = cv2.resize(frame, (width // 2, height // 2))

        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        print(f"Failed to load image {img_path}")

# Close the display window
cv2.destroyAllWindows()
