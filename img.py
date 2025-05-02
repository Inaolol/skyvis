from ultralytics import YOLO

model = YOLO("D:/SkyHawkAI/Testing/Models/best.pt")

result = model("D:\\TUYZ_2024_Data\\frames\\frame_1713.jpg", conf=0.3)


