import queue
import threading
import sys

_messages = queue.Queue()
_started = False
_start_lock = threading.Lock()
_status_lock = threading.Lock()
_status = {"ready": False, "error": None, "voice_name": None, "language": None}


def _set_status(**values):
    with _status_lock:
        _status.update(values)


def get_voice_status():
    with _status_lock:
        return dict(_status)


def _language_tags(voice):
    tags = []
    for value in getattr(voice, "languages", []) or []:
        if isinstance(value, bytes):
            value = value.decode("utf-8", errors="ignore")
        tags.append(str(value).lower())
    tags.extend([
        str(getattr(voice, "id", "")).lower(),
        str(getattr(voice, "name", "")).lower(),
    ])
    return " ".join(tags)


def _select_voice(engine, language):
    voices = engine.getProperty("voices") or []
    if not voices:
        raise RuntimeError("Windows mein koi text-to-speech voice available nahi hai.")

    if language == "Urdu":
        matches = [
            voice for voice in voices
            if any(tag in _language_tags(voice) for tag in ("urdu", "ur-pk", "ur_pk"))
        ]
        if not matches:
            raise RuntimeError(
                "Windows Urdu text-to-speech voice nahi mila. Urdu voice install karein."
            )
    else:
        matches = [
            voice for voice in voices
            if any(tag in _language_tags(voice) for tag in ("en-", "en_", "english"))
        ]
        # Older Windows SAPI voices often have incomplete language metadata.
        # Keep English announcements working by using the system's first voice.
        if not matches:
            matches = [voices[0]]

    selected = matches[0]
    engine.setProperty("voice", selected.id)
    return getattr(selected, "name", selected.id)


def _voice_worker():
    com_initialized = False
    try:
        # SAPI5/pyttsx3 uses COM. Initialize COM explicitly in this worker thread.
        if sys.platform == "win32":
            try:
                import pythoncom
                pythoncom.CoInitialize()
                com_initialized = True
            except ImportError:
                pass

        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", 165)
        engine.setProperty("volume", 1.0)
        _set_status(ready=True, error=None)

        while True:
            item = _messages.get()
            if item is None:
                break
            text, language = item
            try:
                voice_name = _select_voice(engine, language)
                engine.say(text)
                engine.runAndWait()
                _set_status(
                    ready=True, error=None,
                    voice_name=voice_name, language=language
                )
            except Exception as exc:
                _set_status(
                    ready=False, error=str(exc),
                    voice_name=None, language=language
                )
    except Exception as exc:
        _set_status(ready=False, error=f"Voice engine start nahi ho saka: {exc}")
    finally:
        if com_initialized:
            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass


def _start_worker():
    global _started
    with _start_lock:
        if not _started:
            threading.Thread(
                target=_voice_worker,
                daemon=True,
                name="VisionSpeakVoice"
            ).start()
            _started = True


def announce(text, language="English"):
    _start_worker()
    if _messages.qsize() < 3:
        _messages.put((str(text), language))


def test_voice(language="English"):
    sample = (
        "Hello. VisionSpeak voice is working."
        if language == "English"
        else "یہ وائس ٹیسٹ ہے۔"
    )
    announce(sample, language)
