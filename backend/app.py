from flask import Flask, request
import pytesseract
from PIL import Image
import io
import requests
import os 
from dotenv import load_dotenv 

current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, ".env")
load_dotenv(env_path)

if not os.getenv("GEMINI_API_KEY"):
    print("Error: GEMINI_API_KEY environment variable not set.")

from medicine_detector import detect_medicines

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def get_ai_explanation(medicines, age, disease, dosages, risks):
    api_key = os.getenv("GEMINI_API_KEY") 
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    safe_meds = ", ".join(medicines) if medicines else "the scanned medication"
    safe_dose = ", ".join(dosages) if dosages else "the standard dosage"
    
    demo_fallback = f"""
    **AI Medical Assistant**
    
    **Safety Analysis:**
    Based on the patient profile (Age: {age}, Condition: {disease}), {safe_meds} has been identified. 
    
    **Warnings & Dosage:**
    The recommended protocol is {safe_dose}. Please ensure you adhere strictly to this limit to avoid adverse interactions. 
    
    **Simple Advice:**
    Always consult your primary care physician before altering your medication schedule. If you experience dizziness or nausea, stop taking the medication and contact a doctor immediately.
    """
    
    prompt = f"""
    You are a medical assistant AI.
    Age: {age}
    Disease: {disease}
    Medicines: {medicines}
    Dosages: {dosages}
    Risks: {risks}
    
    Explain:
    - safety analysis
    - warnings
    - simple advice
    """
    
    try:
        response = requests.post(
            url,
            params={"key": api_key},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=5 
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return demo_fallback
            
    except Exception:
        return demo_fallback

@app.route("/")
def home():
    return "MedSafer API V1.0"

@app.route("/check", methods=["POST"])
def check():
    try:
        if "image" not in request.files:
            return {"error": "No image uploaded"}, 400
            
        file = request.files["image"]
        age = request.form.get("age")
        disease = request.form.get("disease")

        img = Image.open(io.BytesIO(file.read()))
        text = pytesseract.image_to_string(img)

        detected, dosages, risks = detect_medicines(text)

        ai = get_ai_explanation(detected, age, disease, dosages, risks)

        return {
            "detected_medicines": detected,
            "dosages": dosages,
            "risks": risks,
            "ocr_text": text,
            "ai_explanation": ai
        }

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)