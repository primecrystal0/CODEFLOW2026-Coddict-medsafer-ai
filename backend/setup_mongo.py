import os
from pymongo import MongoClient
from dotenv import load_dotenv

current_dir = os.path.dirname(
    os.path.abspath(__file__)
)

env_path = os.path.join(
    current_dir,
    ".env"
)

load_dotenv(env_path)

MONGO_URI = os.getenv("MONGO_URI")


def setup_database():

    if not MONGO_URI:

        print("MONGO_URI missing")
        return

    try:

        client = MongoClient(MONGO_URI)

        db = client.medsafer_db

        collection = db.indian_meds

        client.admin.command("ping")

        print("MongoDB Connected")

    except Exception as e:

        print(f"Connection Failed: {e}")

        return

    collection.delete_many({})

    medications = [

        {"brand_name": "pan 40", "generic_name": "Pantoprazole", "standard_dosage": "1 tablet before breakfast", "common_risk": "May cause headache or dizziness. Long term use affects bone density."},

        {"brand_name": "gelusil", "generic_name": "Magnesium Hydroxide + Dimethicone", "standard_dosage": "2 teaspoons after meals", "common_risk": "May cause constipation or diarrhea."},

        {"brand_name": "digene", "generic_name": "Magnesium Hydroxide", "standard_dosage": "1-2 tablets chewed after meals", "common_risk": "Do not swallow whole. Chew thoroughly."},

        {"brand_name": "omee", "generic_name": "Omeprazole", "standard_dosage": "1 capsule before breakfast", "common_risk": "May cause stomach pain or gas."},

        {"brand_name": "rantac", "generic_name": "Ranitidine", "standard_dosage": "1 tablet twice a day", "common_risk": "Avoid taking with antacids. May cause headache."},

        {"brand_name": "dolo", "generic_name": "Paracetamol 650mg", "standard_dosage": "1 tablet every 6 hours", "common_risk": "Liver damage if overdose. Avoid alcohol."},

        {"brand_name": "crocin", "generic_name": "Paracetamol 500mg", "standard_dosage": "1 tablet every 4-6 hours", "common_risk": "Liver damage if overdose. Avoid alcohol."},

        {"brand_name": "combiflam", "generic_name": "Ibuprofen + Paracetamol", "standard_dosage": "1 tablet twice a day", "common_risk": "Can cause stomach ulcers. Strictly take with food."},

        {"brand_name": "saridon", "generic_name": "Propyphenazone + Paracetamol", "standard_dosage": "1 tablet for severe headache", "common_risk": "Do not use continuously for more than 3 days."},

        {"brand_name": "meftal spas", "generic_name": "Mefenamic Acid + Dicyclomine", "standard_dosage": "1 tablet for cramps/spasms", "common_risk": "May cause dizziness or blurred vision."},

        {"brand_name": "zerodol-sp", "generic_name": "Aceclofenac + Serratiopeptidase", "standard_dosage": "1 tablet twice daily", "common_risk": "Take with food to avoid gastric irritation."},

        {"brand_name": "cofsils", "generic_name": "Amylmetacresol", "standard_dosage": "1 lozenge every 3 hours", "common_risk": "Do not chew. May cause mild tongue numbness."},

        {"brand_name": "allegra", "generic_name": "Fexofenadine", "standard_dosage": "1 tablet per day", "common_risk": "Avoid taking with fruit juices."},

        {"brand_name": "cetirizine", "generic_name": "Cetirizine", "standard_dosage": "1 tablet at night", "common_risk": "High risk of drowsiness. Do not drive after taking."},

        {"brand_name": "cheston cold", "generic_name": "Cetirizine + Phenylephrine", "standard_dosage": "1 tablet twice a day", "common_risk": "May cause sleepiness and dry mouth."},

        {"brand_name": "sinarest", "generic_name": "Chlorpheniramine + Paracetamol", "standard_dosage": "1 tablet twice a day", "common_risk": "May cause drowsiness. Avoid alcohol."},

        {"brand_name": "benadryl", "generic_name": "Diphenhydramine", "standard_dosage": "2 teaspoons every 6 hours", "common_risk": "Causes severe drowsiness. Not for daytime use."},

        {"brand_name": "telma 40", "generic_name": "Telmisartan", "standard_dosage": "1 tablet daily", "common_risk": "May cause dizziness when standing up quickly."},

        {"brand_name": "amlokind", "generic_name": "Amlodipine", "standard_dosage": "1 tablet daily", "common_risk": "May cause ankle swelling."},

        {"brand_name": "glycomet", "generic_name": "Metformin", "standard_dosage": "1 tablet with meals", "common_risk": "Take with food to avoid stomach upset."},

        {"brand_name": "ecosprin", "generic_name": "Aspirin 75mg", "standard_dosage": "1 tablet daily after food", "common_risk": "High risk of bleeding."},

        {"brand_name": "azithral", "generic_name": "Azithromycin", "standard_dosage": "1 tablet per day for 3-5 days", "common_risk": "Complete the full course."},

        {"brand_name": "augmentin", "generic_name": "Amoxicillin + Clavulanic Acid", "standard_dosage": "1 tablet twice a day", "common_risk": "High risk of diarrhea."},

        {"brand_name": "neurobion forte", "generic_name": "Vitamin B Complex", "standard_dosage": "1 tablet daily", "common_risk": "May turn urine bright yellow."},

        {"brand_name": "shelcal", "generic_name": "Calcium + Vitamin D3", "standard_dosage": "1 tablet daily after meal", "common_risk": "Take with plenty of water."}
    ]

    collection.insert_many(medications)

    collection.create_index("brand_name")

    print(
        f"{len(medications)} medicines added successfully"
    )


if __name__ == "__main__":

    setup_database()