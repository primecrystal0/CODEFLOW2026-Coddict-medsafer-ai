import re

def detect_medicine(text):

    medicines = {
        "Paracetamol": ["paracetamol", "dolo", "acetaminophen", "tylenol"],
        "Ibuprofen": ["ibuprofen", "brufen", "advil", "pain relief", "pain relieg"],
        "Aspirin": ["aspirin", "ecosprin"],
        "Metformin": ["metformin"],
        "Warfarin": ["warfarin"]
    }

    text = text.lower()

    best_match = "Unknown Medicine"
    best_score = 0

    for med, keywords in medicines.items():

        score = 0

        for kw in keywords:

            # fuzzy match (handles OCR mistakes)
            if kw in text:
                score += 2

            # partial match (important for OCR errors)
            elif any(word in text for word in kw.split()):
                score += 1

        if score > best_score:
            best_score = score
            best_match = med

    return best_match