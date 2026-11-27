
import base64
import hashlib
import tempfile
from pathlib import Path

import streamlit as st
from PIL import Image

from utils import load_model, predict_image, process_video


# Page configuration

st.set_page_config(
    page_title="COURTSIDE AI | Basketball Vision",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="auto"
)

BASE_DIR = Path(__file__).parent
HERO_PATH = BASE_DIR / "assets" / "hero.png"


# Custom styling

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

.stApp {
    background: #090e19;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #101a2e;
    border-right: 1px solid #26354e;
}

[data-testid="stSidebar"] * {
    color: #ffffff;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #ffffff !important;
}

.brand {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 35px;
    font-weight: 800;
    letter-spacing: 4px;
    color: #FDB927;
}

.brand-subtitle {
    font-size: 11px;
    letter-spacing: 3px;
    color: #8a9ab5;
    margin-bottom: 25px;
}

.hero {
    min-height: 430px;
    display: flex;
    align-items: center;
    border: 1px solid #34425a;
    border-radius: 24px;
    padding: 45px;
    margin-bottom: 28px;
    overflow: hidden;
}

.hero-content {
    max-width: 510px;
}

.eyebrow {
    color: #FDB927;
    font-size: 12px;
    letter-spacing: 3px;
    font-weight: 700;
    margin-bottom: 18px;
}

.hero-title {
    font-family: 'Barlow Condensed', Impact, sans-serif;
    font-size: clamp(44px, 6vw, 78px);
    font-weight: 800;
    line-height: 0.95;
    color: #ffffff;
    letter-spacing: 1px;
}

.hero-gold {
    color: #FDB927;
}

.hero-description {
    color: #d1d9e6;
    font-size: 16px;
    line-height: 1.7;
    margin-top: 24px;
}

.tech-tag {
    display: inline-block;
    color: #FDB927;
    border: 1px solid #FDB92766;
    background: #FDB92712;
    padding: 7px 14px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    margin: 18px 5px 0 0;
}

.kpi-card {
    background: linear-gradient(135deg, #172642, #10192a);
    border: 1px solid #293953;
    border-top: 3px solid #FDB927;
    border-radius: 15px;
    padding: 25px 20px;
    min-height: 150px;
    margin-bottom: 12px;
}

.kpi-label {
    font-size: 11px;
    letter-spacing: 2px;
    color: #a1b0c8;
    font-weight: 600;
}

.kpi-value {
    font-family: 'Barlow Condensed', Impact, sans-serif;
    font-size: 48px;
    font-weight: 800;
    color: #FDB927;
    line-height: 1.4;
}

.kpi-description {
    color: #8293b0;
    font-size: 12px;
}

.section-heading {
    color: #FDB927;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 32px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-top: 24px;
}

.section-description {
    color: #9daec6;
    font-size: 14px;
    margin-bottom: 22px;
}

.class-card {
    background: #141f33;
    border: 1px solid #2b3c58;
    border-radius: 12px;
    text-align: center;
    padding: 18px 6px;
}

.class-icon {
    font-size: 30px;
}

.class-name {
    color: #ffffff;
    font-size: 13px;
    font-weight: 600;
    margin-top: 8px;
}

.stButton > button {
    background: #FDB927 !important;
    color: #09111e !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
    min-height: 48px;
    width: 100%;
}

.stButton > button:hover {
    background: #ffcf65 !important;
    box-shadow: 0 0 24px #FDB92744;
}

.stDownloadButton > button {
    background: #172642 !important;
    color: #FDB927 !important;
    border: 1px solid #FDB927 !important;
    border-radius: 10px;
    width: 100%;
}

[data-testid="stFileUploaderDropzone"] {
    background: #131e32;
    border: 1px dashed #64748b;
    border-radius: 15px;
}

[data-testid="stFileUploaderDropzone"] * {
    color: #ffffff;
}

[data-testid="stFileUploaderDropzone"] button {
    background: #23334f;
}

.footer {
    text-align: center;
    border-top: 1px solid #26354e;
    margin-top: 40px;
    padding: 25px 10px;
    color: #8293b0;
    font-size: 12px;
    letter-spacing: 1px;
}

.footer strong {
    color: #FDB927;
}

/* Mobile layout: display the entire hero image above the text. */
.hero-mobile-photo {
    display: none;
}

@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .brand {
        font-size: clamp(24px, 7vw, 35px);
        letter-spacing: 2px;
    }

    .brand-subtitle {
        font-size: 10px;
        letter-spacing: 1.5px;
    }

    .hero {
        display: flex;
        flex-direction: column;
        align-items: stretch;
        min-height: 0;
        padding: 0;
        background: linear-gradient(145deg, #101a2e, #090e19) !important;
        border-radius: 20px;
    }

    .hero-mobile-photo {
        display: block;
        width: 100%;
        height: auto;
        object-fit: contain;
        border-bottom: 1px solid #34425a;
    }

    .hero-content {
        box-sizing: border-box;
        width: 100%;
        max-width: none;
        min-width: 0;
        padding: 22px 18px;
        overflow-wrap: break-word;
    }

    .eyebrow {
        font-size: 10px;
        letter-spacing: 1.5px;
        margin-bottom: 14px;
    }

    .hero-title {
        font-size: clamp(34px, 9vw, 50px);
        line-height: 1;
        letter-spacing: 0.5px;
    }

    .hero-description {
        font-size: 14px;
        line-height: 1.6;
        margin-top: 16px;
    }

    .tech-tag {
        font-size: 10px;
        padding: 6px 9px;
        margin: 12px 4px 0 0;
    }

    .hero-credit {
        margin-top: 22px !important;
        font-size: 11px !important;
        letter-spacing: 1.4px !important;
        line-height: 1.6;
    }

    .kpi-value {
        font-size: 38px;
    }

    .section-heading {
        font-size: 26px;
    }
}

</style>
""", unsafe_allow_html=True)


# Header and hero image

st.markdown("""
<div class="brand">🏀 COURTSIDE AI</div>
<div class="brand-subtitle">
    BASKETBALL INTELLIGENCE PLATFORM
</div>
""", unsafe_allow_html=True)

hero_mobile_photo = ""

if HERO_PATH.exists():
    hero_image = base64.b64encode(
        HERO_PATH.read_bytes()
    ).decode()

    hero_mobile_photo = (
        f'<img class="hero-mobile-photo" src="data:image/png;base64,{hero_image}" '
        'alt="Basketball hero image">'
    )

    hero_background = f"""
    background-image:
        linear-gradient(
            90deg,
            rgba(9,14,25,0.98) 0%,
            rgba(9,14,25,0.90) 30%,
            rgba(9,14,25,0.25) 70%,
            rgba(9,14,25,0.05) 100%
        ),
        url('data:image/png;base64,{hero_image}');
    background-size: cover;
    background-position: center right;
    """

else:
    hero_background = """
    background: linear-gradient(
        135deg, #090e19, #193565, #725315
    );
    """

st.markdown(f"""
<div class="hero" style="{hero_background}">
{hero_mobile_photo}
<div class="hero-content">
<div class="eyebrow">THE FUTURE OF SPORTS INTELLIGENCE</div>
<div class="hero-title">
SEE THE GAME.<br>
<span class="hero-gold">BEYOND THE GAME.</span>
</div>
<div class="hero-description">
Transform basketball footage into intelligent visual insights
with advanced object detection and multi-object tracking.
</div>
<span class="tech-tag">YOLO26s</span>
<span class="tech-tag">BYTETRACK</span>
<span class="tech-tag">COMPUTER VISION</span>
<div class="hero-credit" style="margin-top:30px;color:#FDB927;font-size:15px;letter-spacing:2px;font-weight:700;">
DESIGNED & DEVELOPED BY MAI MOHAMMED
</div>
</div>
</div>
""", unsafe_allow_html=True)

# Model performance

metrics = [
    ("TEST mAP50", "98.0%", "Dataset evaluation"),
    ("PEAK TEST F1", "96.0%", "Precision-recall balance"),
    ("OBJECT CLASSES", "05", "Basketball detection"),
    ("MODEL SIZE", "20.3 MB", "Trained checkpoint")
]

for col, (label, value, description) in zip(
    st.columns(4), metrics
):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-description">
                {description}
            </div>
        </div>
        """, unsafe_allow_html=True)


# Sidebar controls

st.sidebar.markdown("## 🏀 CONTROL CENTER")
st.sidebar.markdown("""
**PROJECT DEVELOPER**

### Mai Mohammed
AI & Computer Vision
""")
st.sidebar.caption("Configure your basketball analysis.")

st.sidebar.divider()

confidence = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.10,
    max_value=0.90,
    value=0.30,
    step=0.05
)

tracking = st.sidebar.toggle(
    "Enable Object Tracking",
    value=True
)

st.sidebar.divider()

st.sidebar.markdown("### MODEL PROFILE")

st.sidebar.write("Architecture: YOLO26s")
st.sidebar.write("Training epochs: 50")
st.sidebar.write("Training images: 6,762")
st.sidebar.write("Input size: 640 × 640")
st.sidebar.write("Tracker: ByteTrack")

st.sidebar.divider()

st.sidebar.caption(
    "Lower confidence may improve small-object "
    "detection but can increase false positives."
)


# Supported object classes

st.markdown("""
<div class="section-heading">
    WHAT OUR AI CAN SEE
</div>
<div class="section-description">
    Five basketball-specific object classes.
</div>
""", unsafe_allow_html=True)

classes = [
    ("🏀", "Ball"),
    ("🎯", "FG Attempt"),
    ("✅", "FG Made"),
    ("🗑️", "Hoop"),
    ("⛹️", "Player")
]

for col, (icon, name) in zip(st.columns(5), classes):
    with col:
        st.markdown(f"""
        <div class="class-card">
            <div class="class-icon">{icon}</div>
            <div class="class-name">{name}</div>
        </div>
        """, unsafe_allow_html=True)


# Analysis workspace
# Interactive demo

DEMO_DIR = BASE_DIR / "assets" / "demo"

SAMPLE_IMAGE = DEMO_DIR / "sample.png"
ORIGINAL_VIDEO = DEMO_DIR / "original.mp4"
DETECTED_VIDEO = DEMO_DIR / "detected.mp4"

st.markdown("""
<div class="section-heading">
EXPERIENCE COURTSIDE AI
</div>
<div class="section-description">
Explore basketball computer vision in action.
No upload required.
</div>
""", unsafe_allow_html=True)

demo_image_tab, demo_video_tab = st.tabs([
    "🏀 LIVE IMAGE DEMO",
    "🎬 VIDEO TRACKING SHOWCASE"
])

# Live image inference demo

with demo_image_tab:

    if SAMPLE_IMAGE.exists():

        sample = Image.open(SAMPLE_IMAGE).convert("RGB")

        left, right = st.columns(2)

        with left:
            st.subheader("Sample Image")
            st.image(sample, use_container_width=True)

        if st.button(
            "TRY OUR AI",
            key="run_demo_image"
        ):
            try:
                with st.spinner("Running AI detection..."):

                    model = load_model()

                    st.session_state["demo_prediction"] = (
                        predict_image(model, sample, confidence)
                    )

                    st.session_state["demo_confidence"] = confidence

            except Exception as error:
                st.error(str(error))

        with right:
            st.subheader("AI Detection Results")

            if (
                "demo_prediction" in st.session_state
                and st.session_state.get("demo_confidence")
                == confidence
            ):
                st.image(
                    st.session_state["demo_prediction"],
                    use_container_width=True
                )
            else:
                st.info(
                    "Click TRY OUR AI to run live detection."
                )

    else:
        st.warning("Demo image is unavailable.")


# Preprocessed video demonstration

with demo_video_tab:

    st.caption(
        "Watch a preprocessed demonstration of "
        "basketball detection and multi-object tracking."
    )

    left, right = st.columns(2)

    with left:
        st.subheader("Original Footage")

        if ORIGINAL_VIDEO.exists():
            st.video(str(ORIGINAL_VIDEO))
        else:
            st.warning("Original video is unavailable.")

    with right:
        st.subheader("AI Tracking Results")

        if DETECTED_VIDEO.exists():
            st.video(str(DETECTED_VIDEO))

            st.download_button(
                label="DOWNLOAD DEMO VIDEO",
                data=DETECTED_VIDEO.read_bytes(),
                file_name="courtside_demo.mp4",
                mime="video/mp4",
                key="download_demo"
            )

        else:
            st.warning("Demo video is unavailable.")

st.divider()

st.markdown("""
<div class="section-heading">
    ANALYSIS WORKSPACE
</div>
<div class="section-description">
    Upload your media and experience basketball
    through computer vision.
</div>
""", unsafe_allow_html=True)

image_tab, video_tab = st.tabs([
    "📸 IMAGE DETECTION",
    "🎬 VIDEO ANALYSIS & TRACKING"
])


# Image detection

with image_tab:

    uploaded_image = st.file_uploader(
        "Upload a basketball image",
        type=["jpg", "jpeg", "png"],
        key="image_upload"
    )

    if uploaded_image is not None:

        image_bytes = uploaded_image.getvalue()

        image_key = (
            hashlib.sha256(image_bytes).hexdigest(),
            confidence
        )

        if st.session_state.get("image_key") != image_key:
            st.session_state.pop("image_result", None)
            st.session_state["image_key"] = image_key

        image = Image.open(uploaded_image).convert("RGB")

        left, right = st.columns(2)

        with left:
            st.subheader("Original Image")
            st.image(image, use_container_width=True)

        if st.button(
            "START IMAGE DETECTION",
            key="detect_image"
        ):
            try:
                with st.spinner("Analyzing basketball image..."):

                    model = load_model()

                    st.session_state["image_result"] = (
                        predict_image(model, image, confidence)
                    )

            except Exception as error:
                st.error(str(error))

        with right:
            st.subheader("AI Detection Results")

            if "image_result" in st.session_state:
                st.image(
                    st.session_state["image_result"],
                    use_container_width=True
                )
            else:
                st.info("Run detection to view results.")


# Video detection and tracking

with video_tab:

    uploaded_video = st.file_uploader(
        "Upload basketball footage",
        type=["mp4", "avi", "mov"],
        key="video_upload"
    )

    if uploaded_video is not None:

        video_bytes = uploaded_video.getvalue()

        video_key = (
            hashlib.sha256(video_bytes).hexdigest(),
            confidence,
            tracking
        )

        if st.session_state.get("video_key") != video_key:
            st.session_state.pop("video_result", None)
            st.session_state["video_key"] = video_key

        left, right = st.columns(2)

        with left:
            st.subheader("Original Video")
            st.video(video_bytes)

        if st.button(
            "START VIDEO ANALYSIS",
            key="analyze_video"
        ):

            st.session_state.pop("video_result", None)

            progress = st.progress(
                0.0, text="Processing video frames..."
            )

            try:
                with tempfile.TemporaryDirectory() as tmp:

                    input_path = Path(tmp) / (
                        "input" + Path(uploaded_video.name).suffix
                    )

                    output_path = Path(tmp) / "courtside_result.mp4"

                    input_path.write_bytes(video_bytes)

                    model = load_model()

                    process_video(
                        model=model,
                        input_path=input_path,
                        output_path=output_path,
                        confidence=confidence,
                        tracking=tracking,
                        progress_callback=progress.progress
                    )

                    st.session_state["video_result"] = (
                        output_path.read_bytes()
                    )

                progress.progress(
                    1.0, text="Analysis complete."
                )

                st.success("Video processed successfully!")

            except Exception as error:
                st.error(str(error))

        with right:
            st.subheader("AI Tracking Results")

            if "video_result" in st.session_state:

                st.video(st.session_state["video_result"])

                st.download_button(
                    label="DOWNLOAD ANALYZED VIDEO",
                    data=st.session_state["video_result"],
                    file_name="courtside_result.mp4",
                    mime="video/mp4"
                )

            else:
                st.info("Run video analysis to view results.")


# Footer

st.markdown("""
<div class="footer">
    <strong>COURTSIDE AI</strong>
    <br><br>
    YOLO26s &nbsp; × &nbsp; OpenCV &nbsp; × &nbsp; ByteTrack
    <br><br>
    An independent basketball computer vision project.
    Not affiliated with the NBA or any basketball team.
    <br><br>
    Detection performance may vary on real-world footage.
    Shot-counting statistics are not included.
</div>
""", unsafe_allow_html=True)