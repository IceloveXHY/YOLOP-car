from ultralytics import YOLO

class YOLODetector:
    def __init__(self, model_path, target_classes):
        self.model = YOLO(model_path)
        self.target_classes = target_classes

    def detect(self, frame):
        results = self.model(frame)[0]
        output = []
        for box in results.boxes:
            cls = int(box.cls[0])
            name = self.model.names[cls]
            if name in self.target_classes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                output.append(((x1, y1, x2, y2), name))
        return output
