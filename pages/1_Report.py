import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from fpdf import FPDF
import time

from src.ocr_engine import ocr_image
from src.parser import clean_text
from src.database import load_catalog
from src.scorer import score_items, summarize_results

st.set_page_config(page_title="Report", layout="wide")

# -------- CUSTOM CSS FOR DASHBOARD LOOK --------
st.markdown("""
<style>
.metric-card {
    padding: 20px;
    border-radius: 12px;
    background: linear-gradient(135deg, #1B2A41, #0F172A);
    border: 1px solid #1E293B;
}
.grade-A {color:#00E676; font-size:28px; font-weight:bold;}
.grade-B {color:#8BC34A; font-size:28px; font-weight:bold;}
.grade-C {color:#FFC107; font-size:28px; font-weight:bold;}
.grade-D {color:#F44336; font-size:28px; font-weight:bold;}
.section-divider {
    margin-top:40px;
    margin-bottom:20px;
    border-bottom:1px solid #1E293B;
}
</style>
""", unsafe_allow_html=True)

# -------- SESSION CHECK --------
if "uploaded_files" not in st.session_state:
    st.warning("Please upload receipts first.")
    st.stop()

st.title("📊 Environmental Impact Dashboard")

catalog = load_catalog("data/products.csv")
progress = st.progress(0)
files = st.session_state["uploaded_files"]

all_dfs = []

# -------- PROCESS FILES --------
for i, file in enumerate(files):

    temp_path = Path("data/receipts") / file.name
    with open(temp_path, "wb") as f:
        f.write(file.getbuffer())

    text = ocr_image(temp_path)
    items = clean_text(text)
    results = score_items(items, catalog)
    df, avg_score, high_impact = summarize_results(results)

    if not df.empty:
        all_dfs.append(df)

    progress.progress((i + 1) / len(files))
    time.sleep(0.15)

if not all_dfs:
    st.error("Could not extract valid data.")
    st.stop()

combined_df = pd.concat(all_dfs)
combined_df = combined_df[combined_df["matched_product"] != "UNKNOWN"]

# -------- INTELLIGENCE --------
overall_avg = round(combined_df["impact_score"].mean(), 2)
combined_df["estimated_co2"] = combined_df["impact_score"] * 0.5
weekly_co2 = round(combined_df["estimated_co2"].sum(), 2)
monthly_co2 = round(weekly_co2 * 4, 2)

if overall_avg <= 3:
    grade = "A"
elif overall_avg <= 5:
    grade = "B"
elif overall_avg <= 7:
    grade = "C"
else:
    grade = "D"

high_items = combined_df[combined_df["impact_score"] >= 7]
potential_reduction = round(high_items["estimated_co2"].sum(), 2)

# -------- DASHBOARD CARDS --------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="grade-{grade}">Grade {grade}</div>', unsafe_allow_html=True)
    st.markdown("Environmental Rating")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Average Impact", f"{overall_avg}/10")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Weekly CO₂ (kg)", weekly_co2)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"**Monthly CO₂ Estimate:** {monthly_co2} kg")

if potential_reduction > 0:
    st.success(f"Potential Weekly Reduction: {potential_reduction} kg CO₂")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -------- TABLE --------
st.subheader("📋 Purchase Impact Breakdown")

table_df = combined_df[
    [
        "item_detected",
        "matched_product",
        "impact_score",
        "category",
        "greener_alternative",
        "impact_reason",
    ]
].sort_values(by="impact_score", ascending=False)

st.dataframe(table_df, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -------- IMPROVED GRAPH --------
col_graph, col_suggestion = st.columns([1.3, 1])

with col_graph:
    st.subheader("📈 Impact Trend")

    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(
        combined_df["matched_product"],
        combined_df["impact_score"],
        marker="o",
        linewidth=3,
        markersize=8,
        color="#00E5A8"
    )

    ax.set_ylim(0, 10)
    ax.set_ylabel("Impact Score")
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    st.pyplot(fig)

with col_suggestion:
    st.subheader("🌱 High Impact Suggestions")

    if not high_items.empty:
        for _, row in high_items.iterrows():
            st.markdown(f"""
**{row['matched_product']}** (Score: {row['impact_score']})

Replace with: **{row['greener_alternative']}**
""")
    else:
        st.info("No high-impact items detected.")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -------- PDF --------
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, "Environmental Improvement Guide", ln=True)
    pdf.cell(200, 8, f"Grade: {grade}", ln=True)
    pdf.cell(200, 8, f"Weekly CO2: {weekly_co2} kg", ln=True)
    pdf.cell(200, 8, f"Monthly CO2: {monthly_co2} kg", ln=True)
    pdf.output("EcoReceipt_Guide.pdf")
    return "EcoReceipt_Guide.pdf"

pdf_file = generate_pdf()

with open(pdf_file, "rb") as f:
    st.download_button(
        "📥 Download Improvement Guide (PDF)",
        f,
        file_name="EcoReceipt_Guide.pdf"
    )

if st.button("⬅ Upload More"):
    st.switch_page("app.py")
