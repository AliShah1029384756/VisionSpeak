import queue
import threading
import time

_messages = queue.Queue()
_started = False
_start_lock = threading.Lock()

def _voice_worker():
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", 165)
        engine.setProperty("volume", 1.0)
        while True:
            message = _messages.get()
            if message is None:
                break
            try:
                engine.say(message)
                engine.runAndWait()
            except Exception:
                # Keep the camera running even if Windows speech has a problem.
                pass
    except Exception:
        # Voice is optional; visual detection continues if TTS is unavailable.
        return

def announce(label):
    global _started
    with _start_lock:
        if not _started:
            threading.Thread(target=_voice_worker, daemon=True, name="VisionSpeakVoice").start()
            _started = True
    # Avoid an unbounded queue if the laptop is slow.
    if _messages.qsize() < 3:
        _messages.put(f"{label} detected")
