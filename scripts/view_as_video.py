import cv2
import glob
import time
import os

image_directory = "C:/Users/abdir/Desktop/Visualized"
cv2.namedWindow("Image to video", cv2.WINDOW_NORMAL)

# Desired FPS
desired_fps = 2.0
frame_duration = 1.0 / desired_fps

frame_count = 0
start_time = time.time()

for i in glob.glob(os.path.join(image_directory, "*.jpg")):
    frame_start_time = time.time()

    img = cv2.imread(i)
    
    # FPS calculation
    frame_count += 1
    elapsed_time = frame_start_time - start_time
    if elapsed_time > 0:
        fps = frame_count / elapsed_time
    else:
        fps = 0
    fps_display = f"FPS: {fps:.2f}"

    # Draw FPS on the image
    cv2.putText(img, fps_display, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display image
    cv2.imshow("Image to video", img)
    
    # Key event and break loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Calculate and adjust to the desired frame rate
    time_used = time.time() - frame_start_time
    time_to_wait = frame_duration - time_used
    if time_to_wait > 0:
        time.sleep(time_to_wait)

cv2.destroyAllWindows()
