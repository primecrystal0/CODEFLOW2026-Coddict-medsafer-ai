import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = Image.open("medicine.jpg")

text = pytesseract.image_to_string(img)

print("Extracted Text:")
print(text)

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

print("\nDetected Medicines:")

if detected:
    for med in detected:
        print("-", med)
else:
    print("No known medicine detected")