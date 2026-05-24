from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
from PIL import Image
import io
import os

from ocr_test import extract_text
from medicine_detector import detect_medicine
from interaction_engine import check_interactions

load_dotenv()

app = Flask(__name__)
CORS(app)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ---------------- RISK ----------------
def calculate_risk(text):
    text = text.lower()

    keywords = {
        "overdose": 25,
        "alcohol": 20,
        "pregnancy": 20,
        "danger": 25,
        "bleeding": 30,
        "kidney": 15,
        "liver": 15,
        "heart": 20
    }

    risk = 10

    for k, v in keywords.items():
        if k in text:
            risk += v

    return min(risk, 100)


# ---------------- API ----------------
@app.route("/analyze", methods=["POST"])
def analyze():

    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files["image"]

        # FIXED IMAGE HANDLING
        try:
            image = Image.open(io.BytesIO(file.read())).convert("RGB")
        except:
            return jsonify({"error": "Invalid image file"}), 400

        extracted_text = extract_text(image)
        medicine = detect_medicine(extracted_text)
        warnings = check_interactions(medicine, extracted_text)

        prompt = f"""
        Medicine: {medicine}
        OCR: {extracted_text}

        Give:
        - purpose
        - side effects
        - warnings
        """

        try:
            completion = groq_client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            analysis = completion.choices[0].message.content
        except Exception as e:
            analysis = f"AI error: {str(e)}"

        risk = calculate_risk(analysis)
        risk += len(warnings) * 10
        risk = min(risk, 100)

        return jsonify({
            "medicine": medicine,
            "ocr_text": extracted_text,
            "analysis": analysis,
            "risk": risk,
            "warnings": warnings
        })

    except Exception as e:
        return jsonify({
            "error": "Server crash",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)