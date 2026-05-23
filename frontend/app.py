import streamlit as st
import requests

st.set_page_config(page_title="MedSafer AI")

st.title("💊 MedSafer AI - Drug Safety Checker")


# ---------------- INPUTS ----------------
image = st.file_uploader("Upload Medicine Image", type=["jpg", "png", "jpeg"])
age = st.number_input("Enter Age", 0, 120, value=25)
disease = st.text_input("Enter Disease / Problem")


# ---------------- BUTTON ----------------
if st.button("Analyze"):

    if image is None:
        st.error("Please upload an image")

    else:
        try:
            response = requests.post(
                "http://127.0.0.1:5000/check",
                files={
                    "image": (image.name, image.getvalue(), image.type)
                },
                data={
                    "age": str(age),
                    "disease": disease
                },
                timeout=20
            )

            if response.status_code == 200:
                data = response.json()

                st.subheader("🧠 Medicines Detected")
                st.write(data["detected_medicines"])

                st.subheader("💊 Dosage")
                st.write(data["dosages"])

                st.subheader("⚠️ Risk Level")
                st.write(data["risks"])

                st.subheader("🤖 AI Explanation")
                st.info(data["ai_explanation"])

                st.subheader("📄 OCR Text")
                st.text(data["ocr_text"])

            else:
                st.error("Backend error occurred")

        except Exception:
            st.error("Server not responding. Start backend first.")