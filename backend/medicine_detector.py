import pymongo
import os
from dotenv import load_dotenv
from rapidfuzz import fuzz

load_dotenv()

client = pymongo.MongoClient(
    os.getenv("MONGO_URI")
)

db = client.medsafer_db

collection = db.indian_meds


def detect_medicines(extracted_text):

    detected_medicines = []
    dosages = []
    risks = []

    try:

        search_text = extracted_text.lower().strip()

        medicines = collection.find()

        for med in medicines:

            brand_name = med.get(
                "brand_name",
                ""
            ).lower()

            exact_match = brand_name in search_text

            fuzzy_score = fuzz.partial_ratio(
                brand_name,
                search_text
            )

            if exact_match or fuzzy_score > 80:

                if med["brand_name"] not in detected_medicines:

                    detected_medicines.append(
                        med["brand_name"]
                    )

                    dosages.append(
                        med.get(
                            "standard_dosage",
                            "Not Available"
                        )
                    )

                    risks.append(
                        med.get(
                            "common_risk",
                            "No risk data"
                        )
                    )

        if not detected_medicines:

            return (
                ["Unknown Medicine"],
                ["Not Available"],
                ["No risk data found"]
            )

        return (
            detected_medicines,
            dosages,
            risks
        )

    except Exception as e:

        print(e)

        return (
            ["Detection Failed"],
            ["Unknown"],
            ["Unknown"]
        )