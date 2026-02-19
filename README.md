:

🌍 EcoReceipt — Environmental Impact Analyzer

EcoReceipt is an intelligent receipt analysis dashboard that evaluates the environmental impact of purchased products using OCR, fuzzy matching, and sustainability scoring.

It transforms everyday shopping data into actionable environmental insights.

🚀 Live Demo

(Will add deployment link here after deployment)

📸 Preview

## 📸 Preview

### Upload Interface
![Upload](assets/upload.png)

### Environmental Dashboard
![Dashboard](assets/dashboard.png)

### Impact Trend Analysis
![Trend](assets/trend.png)

✨ Key Features

📷 Upload receipt images (JPG / PNG)

🔎 OCR-based product extraction (Tesseract)

🧠 Fuzzy matching for noisy text correction

🌱 Environmental impact scoring (0–10 scale)

📊 Modern dashboard with grade system (A–D)

🌫 CO₂ emission estimation (weekly + monthly)

🔁 High-impact product replacement suggestions

📄 Downloadable sustainability improvement guide (PDF)

🧠 How It Works

Receipt image → OCR extraction

Text cleaned and parsed

Products matched against sustainability database

Each product assigned:

Impact Score

Category

CO₂ Estimate

Greener Alternative

Environmental Reason

Dashboard calculates:

Environmental Grade

Weekly CO₂ Estimate

Monthly Projection

Potential Reduction

📊 Environmental Model

Estimated CO₂ per item:

Impact Score × 0.5 kg

Environmental Grade:

A → 0–3
B → 3–5
C → 5–7
D → 7–10

🛠 Tech Stack

Python

Streamlit

Tesseract OCR

RapidFuzz

Pandas

Matplotlib

FPDF

📂 Project Structure
EcoReceipt/
│
├── app.py
├── pages/1_Report.py
├── src/
├── data/products.csv
├── .streamlit/config.toml
├── requirements.txt

📦 Installation

Clone the repository:

git clone https://github.com/tanmay-9826/EcoReceipt.git
cd EcoReceipt


Install dependencies:

pip install -r requirements.txt


Run the app:

streamlit run app.py

🌱 Vision

Small shopping decisions create measurable environmental impact.

EcoReceipt helps individuals make data-driven sustainable choices.