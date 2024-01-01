from ultralytics import YOLO

model = YOLO("yolov8n-seg.pt")
model.train(data="data.yaml", epochs=30)
metrics = model.val()
