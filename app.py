import time
import cv2
import streamlit as st
from detector import ObjectDetector
from voice import announce

st.set_page_config(page_title="VisionSpeak", page_icon="👁️", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.5rem; max-width: 1250px;}
.metric-card {background:#111827; padding:16px; border-radius:12px;}
.small-note {color:#64748b; font-size:0.9rem;}
</style>
""", unsafe_allow_html=True)

st.title("👁️ VisionSpeak")
st.caption("Real-time object detection with an offline English voice assistant")

@st.cache_resource
def load_detector():
    return ObjectDetector()

if "camera" not in st.session_state:
    st.session_state.camera = None
if "running" not in st.session_state:
    st.session_state.running = False
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True
if "last_seen" not in st.session_state:
    st.session_state.last_seen = {}

with st.sidebar:
    st.header("Controls")
    st.session_state.voice_enabled = st.toggle("English voice announcements", value=st.session_state.voice_enabled)
    confidence = st.slider("Detection confidence", 0.10, 0.90, 0.45, 0.05)
    st.markdown("---")
    st.markdown("**Camera:** Laptop webcam (index 0)")
    st.markdown("**Mode:** Local / offline after setup")
    st.markdown("---")
    st.caption("Tip: Keep the object well-lit and clearly visible.")

col_a, col_b = st.columns([1, 1])
with col_a:
    if st.button("▶ Start camera", type="primary", use_container_width=True, disabled=st.session_state.running):
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not camera.isOpened():
            camera.release()
            st.error("Could not open the webcam. Close other camera apps and try again.")
        else:
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
            st.session_state.camera = camera
            st.session_state.running = True
            st.rerun()
with col_b:
    if st.button("■ Stop camera", use_container_width=True, disabled=not st.session_state.running):
        st.session_state.running = False
        if st.session_state.camera is not None:
            st.session_state.camera.release()
            st.session_state.camera = None
        st.rerun()

video_area = st.empty()
status_area = st.empty()
detector = load_detector()

@st.fragment(run_every=0.08)
def live_view():
    if not st.session_state.running or st.session_state.camera is None:
        video_area.info("Press **Start camera** to begin live detection.")
        return

    ok, frame = st.session_state.camera.read()
    if not ok:
        status_area.error("Camera frame could not be read. Stop and restart the camera.")
        return

    annotated, detections = detector.detect(frame, confidence)
    video_area.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)

    now = time.time()
    names_now = []
    for item in detections:
        label = item["label"]
        names_now.append(label)
        previous = st.session_state.last_seen.get(label, 0)
        if st.session_state.voice_enabled and now - previous >= 4.0:
            announce(label)
            st.session_state.last_seen[label] = now

    unique_names = sorted(set(names_now))
    if unique_names:
        status_area.success("Detected: " + " · ".join(unique_names))
    else:
        status_area.info("Looking for objects…")

live_view()

st.markdown("---")
st.markdown("**Objects supported:** Person, mobile phone, laptop, bottle, glass (wine-glass class), book, chair, table (dining-table class), keyboard, mouse, clock, scissors and remote.")
st.caption("VisionSpeak is a school exhibition demonstration. Detection is approximate and depends on lighting, camera quality and object angle.")
