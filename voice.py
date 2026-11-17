import queue
import threading

_messages = queue.Queue()
_started = False
_start_lock = threading.Lock()
_status_lock = threading.Lock()
_status = {"ready": False, "error": None, "voice_name": None, "language": None}


def _language_tags(voice):
    tags = []
    for value in getattr(voice, "languages", []) or []:
        if isinstance(value, bytes):
            value = value.decode("utf-8", errors="ignore")
        tags.append(str(value).lower())
    tags.extend([str(getattr(voice, "id", "")).lower(),
                 str(getattr(voice, "name", "")).lower()])
    return " ".join(tags)


def _select_voice(engine, language):
    voices = engine.getProperty("voices") or []
    wanted = "ur" if language == "Urdu" else "en"
    matches = []
    for voice in voices:
        tags = _language_tags(voice)
        if wanted == "ur":
            if "urdu" in tags or "ur-pk" in tags or "ur_pk" in tags:
                matches.append(voice)
        elif "en-" in tags or "en_" in tags or "english" in tags:
            matches.append(voice)
    if not matches:
        if language == "Urdu":
            raise RuntimeError(
                "Windows Urdu text-to-speech voice nahi mila. Settings > Time & language > Speech mein Urdu voice install karein."
            )
        raise RuntimeError(
            "Windows English text-to-speech voice nahi mila. Windows Speech settings mein English voice install karein."
        )
    selected = matches[0]
    engine.setProperty("voice", selected.id)
    return getattr(selected, "name", selected.id)


def _set_status(**values):
    with _status_lock:
        _status.update(values)


def get_voice_status():
    with _status_lock:
        return dict(_status)


def _voice_worker():
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", 165)
        engine.setProperty("volume", 1.0)
        _set_status(ready=True, error=None, voice_name=None, language=None)

        while True:
            item = _messages.get()
            if item is None:
                break
            text, language = item
            try:
                voice_name = _select_voice(engine, language)
                _set_status(ready=True, error=None, voice_name=voice_name, language=language)
                engine.say(text)
                engine.runAndWait()
            except Exception as exc:
                _set_status(ready=False, error=str(exc), voice_name=None, language=language)
    except Exception as exc:
        _set_status(ready=False, error=f"Voice engine start nahi ho saka: {exc}")


def _start_worker():
    global _started
    with _start_lock:
        if not _started:
            threading.Thread(target=_voice_worker, daemon=True, name="VisionSpeakVoice").start()
            _started = True


def announce(text, language="English"):
    _start_worker()
    if _messages.qsize() < 3:
        _messages.put((str(text), language))


def test_voice(language="English"):
    sample = "Hello. VisionSpeak voice is working." if language == "English" else "یہ وائس ٹیسٹ ہے۔"
    announce(sample, language)
