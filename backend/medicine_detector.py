def detect_medicine(text):

    medicines = {
        "Paracetamol": ["paracetamol", "acetaminophen", "dolo", "crocin"],
        "Ibuprofen": ["ibuprofen", "brufen", "advil"],
        "Aspirin": ["aspirin", "ecosprin"],
        "Metformin": ["metformin", "glucophage"],
        "Warfarin": ["warfarin", "coumadin"]
    }

    text = text.lower()

    best_match = "Unknown Medicine"
    confidence = 0

    for med, keywords in medicines.items():

        score = 0

        for word in keywords:
            if word in text:
                score += 1

        if score > confidence:
            confidence = score
            best_match = med

    return best_match