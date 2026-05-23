from flask import Flask
import pytesseract
from PIL import Image

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.route("/")
def home():
    return "MedSafer AI Backend Running"

@app.route("/check")
def check():

    img = Image.open("medicine.jpg")

    text = pytesseract.image_to_string(img)

    known_medicines = [
        "Paracetamol",
        "Ibuprofen",
        "Aspirin",
        "Warfarin"
    ]

    detected = []

    for med in known_medicines:
        if med.lower() in text.lower():
            detected.append(med)

    dangerous_pairs = {
        ("Paracetamol", "Ibuprofen"): "May increase liver stress.",
        ("Aspirin", "Warfarin"): "High bleeding risk!"
    }

    warning = "No dangerous interactions found."

    for pair, message in dangerous_pairs.items():
        if pair[0] in detected and pair[1] in detected:
            warning = message

    return {
        "detected_medicines": detected,
        "warning": warning,
        "ocr_text": text
    }

if __name__ == "__main__":
    app.run(debug=True)