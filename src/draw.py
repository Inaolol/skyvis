import cv2
import numpy as np

# Create a blank white image (you can load an actual image here if needed)
# image = np.ones((100, 300, 3), dtype=np.uint8) * 255

image_path = "./_images/frame_1000.jpg"
image = cv2.imread(image_path)

if image is not None:    
    # Bounding box coordinates
    top_left_x, top_left_y = 830, 820
    bottom_right_x, bottom_right_y = 924, 1026

   

    # Draw the bounding box
    color = (0, 255, 0)  # Green color
    thickness = 2
    cv2.rectangle(image, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), color, thickness)
    
     # Resize the frame to a quarter of its original size
    height, width = image.shape[:2]
    frame = cv2.resize(image, (width // 2, height // 2))

    # Display the image
    cv2.imshow("Bounding Box", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
