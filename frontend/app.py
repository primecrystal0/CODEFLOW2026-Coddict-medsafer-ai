import streamlit as st
from PIL import Image
import requests
import pyttsx3
import time
import os

st.set_page_config(
    page_title="MedSafer AI",
    layout="wide",
    page_icon="💊"
)

# ---------------- CSS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(BASE_DIR, "styles.css")

if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1 class='main-title'>💊 MedSafer AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI Powered Drug Interaction Warning System</p>", unsafe_allow_html=True)

# ---------------- ELDERLY MODE ----------------
elderly_mode = st.toggle("👴 Elderly Friendly Mode")

if elderly_mode:
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 24px !important;
    }
    button {
        height: 70px !important;
        font-size: 24px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- PATIENT INFO ----------------
st.subheader("🧑 Patient Information")

age = st.number_input("Enter Age", min_value=1, max_value=120, value=25)

conditions = st.multiselect(
    "Pre-existing conditions",
    ["None", "Diabetes", "Heart Disease", "Liver Disease", "Kidney Disease", "Asthma"]
)

# ---------------- INPUT ----------------
uploaded = st.file_uploader("📸 Upload Pill Bottle", type=["png", "jpg", "jpeg"])
camera = st.camera_input("📷 Or Scan Using Camera")

image_file = uploaded if uploaded else camera

# ---------------- PROCESS ----------------
if image_file:

    image = Image.open(image_file)
    st.image(image, use_container_width=True)

    with st.spinner("🧠 AI analyzing medicine..."):
        time.sleep(1)

        files = {
            "image": ("image.jpg", image_file.getvalue(), "image/jpeg")
        }

        data = {
            "age": age,
            "conditions": ",".join(conditions)
        }

        try:
            response = requests.post(
                "http://localhost:5000/analyze",
                files=files,
                data=data,
                timeout=60
            )

            st.write("STATUS:", response.status_code)

            if response.status_code != 200:
                st.error("Backend Error")
                st.write(response.text)
                st.stop()

            result = response.json()

        except Exception as e:
            st.error(f"Backend not reachable: {e}")
            st.stop()

    # ---------------- OUTPUT ----------------
    st.subheader("💊 Medicine")
    st.write(result.get("medicine"))

    st.subheader("📄 OCR Text")
    st.code(result.get("ocr_text"))

    st.subheader("🧠 AI Analysis")
    st.write(result.get("analysis"))

    st.subheader("⚠️ Risk Score")
    risk = result.get("risk", 0)

    st.progress(risk / 100)

    if risk < 40:
        st.success(f"LOW RISK ({risk}%)")
    elif risk < 70:
        st.warning(f"MEDIUM RISK ({risk}%)")
    else:
        st.error(f"HIGH RISK ({risk}%)")

    # ---------------- WARNINGS ----------------
    warnings = result.get("warnings", [])

    if warnings:
        st.subheader("🚨 Drug Interaction Warnings")

        engine = pyttsx3.init()
        speech = "Warning detected."

        for w in warnings:
            st.warning(f"{w['medicine']} + {w['interaction']} → {w['warning']}")
            speech += w["warning"]

        engine.say(speech)
        engine.runAndWait()