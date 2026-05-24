from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import base64
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from medicine_detector import detect_medicines

app = Flask(__name__)
CORS(app)

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_ai_explanation(medicines, age, disease, dosages, risks):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    You are a medical safety assistant.

    Patient Information:
    - Age: {age}
    - Existing Disease: {disease}

    Detected Medicines:
    {medicines}

    Dosages:
    {dosages}

    Risks:
    {risks}

    Give:
    1. Simple medicine safety advice
    2. Possible side effects
    3. Whether doctor consultation is needed
    4. Keep response short and beginner-friendly
    """

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 300
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:

            data = response.json()

            return data["choices"][0]["message"]["content"]

        else:
            return "AI advice currently unavailable."

    except:
        return "AI advice currently unavailable."


@app.route("/")
def home():

    return jsonify({
        "status": "success",
        "message": "MEDSAFER AI Backend Running 🚀"
    })


@app.route("/check", methods=["POST"])
def check():

    try:

        if "image" not in request.files:

            return jsonify({
                "status": "error",
                "message": "No image uploaded"
            }), 400

        file = request.files["image"]

        age = request.form.get("age", "65")
        disease = request.form.get("disease", "None")

        file_bytes = file.read()

        img = Image.open(BytesIO(file_bytes))

        img = img.convert("RGB")

        img.thumbnail((1000, 1000))

        buffer = BytesIO()

        img.save(
            buffer,
            format="JPEG",
            quality=90
        )

        b64_img = base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.2-11b-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """
                            Extract ONLY medicine brand names from this image.

                            Rules:
                            - Return comma separated medicine names
                            - Ignore random text
                            - Ignore dosage
                            - Ignore packaging text
                            - Return 'unknown' if nothing found
                            """
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64_img}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.1,
            "max_tokens": 100
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=40
        )

        if response.status_code == 200:

            result = response.json()

            extracted_text = (
                result["choices"][0]["message"]["content"]
                .strip()
                .lower()
            )

        else:

            extracted_text = "unknown"

        detected, dosages, risks = detect_medicines(
            extracted_text
        )

        ai_text = get_ai_explanation(
            detected,
            age,
            disease,
            dosages,
            risks
        )

        return jsonify({

            "status": "success",

            "detected_medicines": detected,

            "dosages": dosages,

            "risks": risks,

            "ocr_text": extracted_text,

            "ai_explanation": ai_text

        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )