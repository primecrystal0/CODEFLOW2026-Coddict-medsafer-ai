import streamlit as st
import requests
import pyttsx3
import threading
from PIL import Image
import io

# Must be the very first Streamlit command
st.set_page_config(page_title="MedSafer AI", page_icon="💊", layout="centered")

# --- CUSTOM CSS FOR ELDERLY UI ---
# This makes everything massive and highly readable
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 22px !important;
    }
    h1 {
        font-size: 45px !important;
        color: #1E88E5;
    }
    h3 {
        font-size: 30px !important;
    }
    .stButton>button {
        width: 100%;
        height: 80px;
        font-size: 30px !important;
        font-weight: bold;
        background-color: #D32F2F !important;
        color: white !important;
        border-radius: 12px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #B71C1C !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TEXT-TO-SPEECH ENGINE ---
def speak_warning(text):
    """Runs the voice engine in the background so it doesn't freeze the screen."""
    def _speak():
        try:
            engine = pyttsx3.init()
            # Slow down the voice slightly for elderly comprehension
            engine.setProperty('rate', 150) 
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Voice engine failed: {e}")
            
    threading.Thread(target=_speak, daemon=True).start()

# --- APP LAYOUT ---
st.title("💊 MedSafer AI")
st.markdown("**Drug Safety Checker for Seniors**")
st.write("---")

# Inputs
uploaded_file = st.file_uploader("📸 Upload a picture of your medicine bottle:", type=["jpg", "jpeg", "png"])

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("👤 Patient Age:", min_value=1, max_value=120, value=65)
with col2:
    disease = st.text_input("❤️ Current Health Condition:", placeholder="e.g., High Blood Pressure")

st.write("---")

# The Giant Analyze Button
if st.button("🔍 ANALYZE MEDICINE"):
    if uploaded_file is None:
        st.error("⚠️ Please upload an image of your medicine first.")
    else:
        with st.spinner("🤖 AI is reading the label... please wait..."):
            try:
                # Prepare the image and data to send to your Flask backend
                files = {"image": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {"age": age, "disease": disease}
                
                # Call your local backend API
                response = requests.post("http://127.0.0.1:5000/check", files=files, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("✅ Analysis Complete!")
                    
                    # 1. Show the extracted data cleanly
                    st.subheader("🩺 What we found:")
                    st.info(f"**Detected Medicine:** {', '.join(result.get('detected_medicines', [])) or 'None found'}")
                    st.warning(f"**Standard Dosage:** {', '.join(result.get('dosages', [])) or 'Unknown'}")
                    
                    # 2. Show the AI Explanation
                    st.subheader("🗣️ Doctor's Advice:")
                    ai_text = result.get('ai_explanation', 'No advice generated.')
                    st.write(ai_text)
                    
                    # 🔥 TRIGGER THE VOICE!
                    speak_warning(ai_text)
                    
                    # 3. Hide the messy raw data for the judges in an expander
                    with st.expander("🛠️ View Raw Scanner Data (For Judges)"):
                        st.text(result.get('ocr_text', 'No text extracted.'))
                        
                else:
                    st.error(f"Backend Error: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Failed to connect to the backend server. Is it running? Error: {e}")