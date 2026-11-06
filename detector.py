from pathlib import Path
import cv2
from ultralytics import YOLO

MODEL_PATH = Path(__file__).parent / "models" / "yolo11n.pt"

# COCO class names supported by the pretrained YOLO11n model.
# "Glass" and "Table" are display aliases for wine glass and dining table.
DISPLAY_NAMES = {
    "person": "Person",
    "cell phone": "Mobile phone",
    "laptop": "Laptop",
    "bottle": "Bottle",
    "wine glass": "Glass",
    "book": "Book",
    "chair": "Chair",
    "dining table": "Table",
    "keyboard": "Keyboard",
    "mouse": "Mouse",
    "clock": "Clock",
    "scissors": "Scissors",
    "remote": "Remote",
}

class ObjectDetector:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "YOLO model is missing. Run setup.bat while connected to the internet "
                "to download models/yolo11n.pt before using VisionSpeak offline."
            )
        self.model = YOLO(str(MODEL_PATH))
        self.allowed = set(DISPLAY_NAMES)

    def detect(self, frame, confidence=0.45):
        results = self.model.predict(
            source=frame,
            conf=confidence,
            imgsz=640,
            device="cpu",
            verbose=False
        )
        result = results[0]
        annotated = result.plot()
        detections = []

        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls[0].item())
                original_name = self.model.names[class_id]
                if original_name not in self.allowed:
                    continue
                detections.append({
                    "label": DISPLAY_NAMES[original_name],
                    "confidence": float(box.conf[0].item())
                })

        return annotated, detections
