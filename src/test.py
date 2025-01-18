from ultralytics import YOLO
import glob

model = YOLO("C:/Users/abdir/Downloads/WALDO30_yolov8m_640x640.pt")
image = glob.glob("C:/Users/abdir/Pictures/_images/*.jpg")

for img in image:
    results = model(img, show=True)