medicine_db = {
    "Paracetamol": {
        "risk": "Low",
        "dosage": "500mg every 6–8 hours"
    },
    "Ibuprofen": {
        "risk": "Medium",
        "dosage": "200–400mg after food"
    },
    "Aspirin": {
        "risk": "High",
        "dosage": "75–150mg daily (doctor supervision required)"
    },
    "Warfarin": {
        "risk": "High",
        "dosage": "Strict medical supervision required"
    }
}


def detect_medicines(text):
    detected = []
    dosages = []
    risks = []

    for med in medicine_db:
        if med.lower() in text.lower():
            detected.append(med)
            dosages.append(medicine_db[med]["dosage"])
            risks.append(medicine_db[med]["risk"])

    return detected, dosages, risks