# VisionSpeak 👁️

**Real-Time AI Object Detection with Offline English Voice Announcements**

VisionSpeak uses a laptop webcam and a pretrained YOLO11n model to recognize selected everyday objects, draw detection boxes, display object names, and speak short English announcements.

## Features
- Live laptop webcam detection
- Object names and bounding boxes
- Offline English speech using Windows text-to-speech
- Adjustable confidence threshold
- CPU mode; no NVIDIA GPU required
- Runs locally on Windows 10
- No custom model training required

## Supported objects
Person, mobile phone, laptop, bottle, glass, book, chair, table, keyboard, mouse, clock, scissors and remote.

**Model limitations:** The pretrained COCO model recognizes "wine glass" and "dining table"; VisionSpeak displays these as "Glass" and "Table". It does not include a general-purpose pen class, and may not recognize every type of glass or table.

## Windows 10 setup

### 1. Install Python
Install Python 3.11 (64-bit) and enable **Add Python to PATH**.

### 2. Download the project
Download this repository as a ZIP and extract it, or clone it:
```bat
git clone https://github.com/AliShah1029384756/VisionSpeak.git
cd VisionSpeak
```

### 3. One-time setup (internet required)
Double-click `setup.bat`. It creates a virtual environment, installs the packages and downloads the YOLO11n model into `models/`.

Complete this setup before exhibition day while internet is available.

### 4. Run
Double-click `run.bat`. The local dashboard opens in your browser. Press **Start camera**.

After setup and model download, the application works without internet.

## Exhibition checklist
- Run `setup.bat` before exhibition day.
- Test the webcam and speakers once.
- Allow desktop apps to access the camera in Windows privacy settings.
- Keep the laptop plugged in and close unnecessary apps.
- Test in the same lighting planned for the exhibition.

## Troubleshooting
- **Camera not opening:** Close Zoom/Teams/Camera app and restart VisionSpeak. Check Windows camera permissions.
- **No speech:** Check speaker volume and Windows speech settings. Visual detection works independently.
- **Slow detection:** Close heavy apps and reduce camera resolution if needed.
- **Model missing:** Connect to the internet and run `setup.bat` again.

## Technology
Python · Streamlit · OpenCV · Ultralytics YOLO11n · pyttsx3

## License note
This project uses the Ultralytics YOLO model/package. Review the [Ultralytics licensing terms](https://www.ultralytics.com/license) before redistribution or commercial use. This repository is intended for an educational exhibition.
