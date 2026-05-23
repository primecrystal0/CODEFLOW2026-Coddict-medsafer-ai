# 💊 MedSafer AI: Drug Safety Checker for Seniors

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Backend-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red.svg)
![Gemini AI](https://img.shields.io/badge/AI-Gemini%202.0%20Flash-orange.svg)

## 📌 The Problem
Elderly patients frequently manage multiple medications, leading to a high risk of adverse drug interactions. Medical jargon on prescription bottles is often too small to read and too complex to understand, leaving seniors vulnerable to dangerous side effects.

## 💡 The Solution
MedSafer AI is an end-to-end healthcare dashboard tailored specifically for elderly accessibility. By simply uploading a photo of a medicine bottle, the app securely reads the label and cross-references it with the patient's age and health conditions to deliver simple, localized, and spoken medical advice.

## ✨ Key Features
* **👵 Elderly-First UI:** High-contrast dashboard with massive text and buttons.
* **🗣️ Voice Engine Integration:** Automatically reads AI warnings out loud for visually impaired patients.
* **🔒 Privacy-First OCR:** Uses local Tesseract OCR to extract text so raw images never leave the device.
* **🧠 Gemini 2.0 Translation:** Converts complex medical interactions into highly readable, empathetic advice.
* **🛡️ Smart Fallback Engine:** Built-in "Demo Insurance" that generates dynamic fallback safety data if the live API experiences rate limits, guaranteeing 100% uptime.

## 🏗️ Technical Architecture
* **Frontend:** Streamlit (Python) + Custom CSS + `pyttsx3` (Offline Text-to-Speech)
* **Backend:** Flask API handling concurrent requests.
* **Computer Vision:** Tesseract OCR (Optical Character Recognition).
* **AI Engine:** Google Gemini 2.0 Flash API via `requests`.

## 🚀 How to Run Locally

**1. Clone the repository and install dependencies:**
```bash
pip install flask streamlit python-dotenv pytesseract pillow requests pyttsx3