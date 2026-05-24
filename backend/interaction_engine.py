medicine_db = {
    "Paracetamol": {
        "interacts_with": ["alcohol"],
        "severity": "Medium",
        "warning": "May cause liver damage with alcohol."
    },

    "Ibuprofen": {
        "interacts_with": ["warfarin"],
        "severity": "High",
        "warning": "Can increase bleeding risk."
    },

    "Aspirin": {
        "interacts_with": ["ibuprofen"],
        "severity": "Medium",
        "warning": "May reduce heart protection."
    },

    "Metformin": {
        "interacts_with": ["alcohol"],
        "severity": "High",
        "warning": "Can cause lactic acidosis."
    }
}


def check_interactions(medicine_name, text):

    warnings = []

    text = text.lower()

    for med, info in medicine_db.items():

        if med.lower() in medicine_name.lower():

            for interaction in info["interacts_with"]:

                if interaction in text:

                    warnings.append({
                        "medicine": med,
                        "interaction": interaction,
                        "severity": info["severity"],
                        "warning": info["warning"]
                    })

    return warnings