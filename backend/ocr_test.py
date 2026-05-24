import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

img = Image.open("test.jpg")

img = img.convert("L")

contrast = ImageEnhance.Contrast(img)
img = contrast.enhance(2.5)

sharpener = ImageEnhance.Sharpness(img)
img = sharpener.enhance(2.0)

img = img.filter(ImageFilter.MedianFilter())

img = ImageOps.autocontrast(img)

custom_config = r'--oem 3 --psm 6'

text = pytesseract.image_to_string(
    img,
    config=custom_config
)

print("\n============================")
print(" EXTRACTED TEXT ")
print("============================\n")

print(text)

print("\n============================")