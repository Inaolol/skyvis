from ultralytics import YOLO
import glob

model = YOLO("yolov8m_640x640.pt")
image = glob.glob("./Pictures/_images/*.jpg")

for img in image:
    results = model(img, show=True)