from pathlib import Path
from urllib.request import urlretrieve

MODEL_DIR = Path(__file__).parent / "models"
MODEL_DIR.mkdir(exist_ok=True)
MODEL_FILE = MODEL_DIR / "yolo11n.pt"
MODEL_URL = "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt"

if MODEL_FILE.exists():
    print(f"Model already exists: {MODEL_FILE}")
else:
    print("Downloading YOLO11n model (one-time internet connection required)...")
    urlretrieve(MODEL_URL, MODEL_FILE)
    print(f"Model saved to: {MODEL_FILE}")
print("You can now run VisionSpeak offline.")
