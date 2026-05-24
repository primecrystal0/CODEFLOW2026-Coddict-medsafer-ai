




import streamlit as st
import requests
from PIL import Image
import time
import pyttsx3
import tempfile
import os

st.set_page_config(
    page_title="MedSafer AI",
    page_icon="💊",
    layout="wide"
)

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #020617
    );
    color: white;
}

.hero-title {
    font-size: 68px;
    font-weight: 800;
    text-align: center;
    color: #38bdf8;
    margin-bottom: 10px;
}

.hero-subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 24px;
    margin-bottom: 40px;
}

.card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.15);
    padding: 30px;
    border-radius: 28px;
    backdrop-filter: blur(16px);
    box-shadow: 0px 10px 35px rgba(0,0,0,0.5);
}

.result-card {
    background: linear-gradient(
        135deg,
        #111827,
        #1e293b
    );

    border: 2px solid #38bdf8;

    padding: 30px;

    border-radius: 28px;

    margin-top: 20px;
}

.big-text {
    font-size: 24px;
    font-weight: 600;
}

.safe-box {
    background: #052e16;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #22c55e;
    margin-top: 20px;
}

.warning-box {
    background: #450a0a;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #ef4444;
    margin-top: 20px;
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 50px;
    font-size: 18px;
}

.stButton>button {
    background: linear-gradient(to right, #0ea5e9, #2563eb);
    color: white;
    border-radius: 15px;
    border: none;
    padding: 14px;
    font-size: 18px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


def text_to_speech(text):

    engine = pyttsx3.init()

    engine.setProperty('rate', 145)

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    engine.save_to_file(text, temp_file.name)

    engine.runAndWait()

    return temp_file.name


st.markdown(
    "<div class='hero-title'>💊 MedSafer AI</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='hero-subtitle'>
    AI Medicine Detection & Elderly Safety Assistant
    </div>
    """,
    unsafe_allow_html=True
)

left, right = st.columns([1, 1])

with left:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📸 Upload or Scan Medicine")

    uploaded_file = st.file_uploader(
        "Upload medicine image",
        type=["png", "jpg", "jpeg"]
    )

    camera_file = st.camera_input(
        "Or scan medicine live"
    )

    age = st.number_input(
        "Patient Age",
        min_value=1,
        max_value=120,
        value=65
    )

    disease = st.text_input(
        "Existing Disease",
        placeholder="Diabetes, BP, Asthma..."
    )

    emergency_mode = st.toggle(
        "🚨 Elderly Emergency Mode"
    )

    analyze = st.button(
        "🔍 Analyze Medicine",
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

with right:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("🧠 AI Analysis")

    image_source = uploaded_file if uploaded_file else camera_file

    if image_source and analyze:

        image = Image.open(image_source)

        st.image(
            image,
            caption="Medicine Image",
            use_container_width=True
        )

        with st.spinner("Analyzing medicine with AI..."):

            time.sleep(1)

            files = {
                "image": image_source.getvalue()
            }

            data = {
                "age": age,
                "disease": disease
            }

            try:

                response = requests.post(
                    "http://127.0.0.1:5000/check",
                    files=files,
                    data=data,
                    timeout=60
                )

                if response.status_code == 200:

                    res = response.json()

                    medicines = res.get(
                        "detected_medicines",
                        []
                    )

                    dosages = res.get(
                        "dosages",
                        []
                    )

                    risks = res.get(
                        "risks",
                        []
                    )

                    ai_text = res.get(
                        "ai_explanation",
                        "No AI response"
                    )

                    ocr_text = res.get(
                        "ocr_text",
                        ""
                    )

                    st.markdown(
                        """
                        <div class='result-card'>
                        <div class='big-text'>
                        ✅ Analysis Complete
                        </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    for i in range(len(medicines)):

                        st.markdown(
                            f"""
                            ### 💊 {medicines[i]}

                            ## Dosage
                            {dosages[i]}

                            ## Risk
                            {risks[i]}
                            """
                        )

                    if emergency_mode:

                        st.markdown(
                            """
                            <div class='warning-box'>
                            🚨 Elderly mode enabled. Please consult a doctor before combining medicines.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    else:

                        st.markdown(
                            """
                            <div class='safe-box'>
                            ✅ Standard medicine safety mode active.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with st.expander("📄 OCR Extracted Text"):

                        st.write(ocr_text)

                    st.markdown("## 🤖 AI Safety Advice")

                    st.info(ai_text)

                    if st.button("🔊 Read AI Advice"):

                        audio_path = text_to_speech(ai_text)

                        audio_file = open(audio_path, 'rb')

                        st.audio(audio_file.read())

                        audio_file.close()

                        os.remove(audio_path)

                else:

                    st.error(
                        "Backend returned an error"
                    )

            except Exception as e:

                st.error(f"Connection Error: {e}")

    else:

        st.info(
            "Upload or scan a medicine image to begin analysis."
        )

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")


st.markdown(
    """
    <div class='footer'>
    🚀 Built for 36 Hour Hackathon | AI + OCR + Elderly Healthcare
    </div>
    """,
    unsafe_allow_html=True
)
