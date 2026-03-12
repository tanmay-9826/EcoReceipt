import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF

from core.ocr_engine import ocr_image
from core.parser import clean_items
from core.database import load_catalog
from core.scorer import match_products, summarize_results

st.set_page_config(page_title="Environmental Impact Dashboard", layout="wide")

# -------- CUSTOM CSS FOR DASHBOARD --------
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
        margin-top:40px; margin-bottom:20px;
        border-bottom:1px solid #1E293B;
    }
</style>
""", unsafe_allow_html=True)

if "uploaded_files" not in st.session_state:
    st.warning("Please upload receipts first.")
    st.stop()

st.title("📊 Environmental Impact Dashboard")

catalog = load_catalog("data/products.csv")
files = st.session_state["uploaded_files"]
all_dfs = []

# -------- PROCESS FILES IN MEMORY (Cloud Safe) --------
for file in files:
    file_bytes = file.read()
    file_stream = BytesIO(file_bytes)
    
    with st.spinner(f"Analyzing {file.name}..."):
        text = ocr_image(file_stream)
        items = clean_items(text)
        results = match_products(items, catalog)
        df, _, _ = summarize_results(results)
        
        if not df.empty:
            all_dfs.append(df)

if not all_dfs:
    st.error("Could not extract valid data.")
    st.stop()

combined_df = pd.concat(all_dfs)
combined_df = combined_df[combined_df["matched_product"] != "UNKNOWN"]

if combined_df.empty:
    st.warning("No known products found.")
    st.stop()

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

# -------- ACCORDION TABLE --------
st.subheader("🛒 Scanned Items Analysis")
for _, row in combined_df.iterrows():
    with st.expander(f"🧾 {row['matched_product']} (Impact: {row['impact_score']}/10)"):
        st.write(f"**Category:** {row['category']}")
        st.write(f"**Why it matters:** {row['impact_reason']}")
        st.success(f"**Greener Alternative:** {row['greener_alternative']}")
        st.write(f"**Why switch?** {row['alternative_reason']}")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -------- PDF GENERATION --------
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, "Environmental Improvement Guide", ln=True)
    pdf.cell(200, 8, f"Grade: {grade}", ln=True)
    pdf.cell(200, 8, f"Weekly CO2: {weekly_co2} kg", ln=True)
    pdf.cell(200, 8, f"Monthly CO2: {monthly_co2} kg", ln=True)
    pdf.ln(10)
    
    if not high_items.empty:
        for _, r in high_items.iterrows():
            instruction = (
                f"You purchased {r['matched_product']} (Impact Score: {r['impact_score']}).\n"
                f"Why it matters: {r['impact_reason']}\n"
                f"Consider replacing it with {r['greener_alternative']}.\n"
                f"Why this helps: {r['alternative_reason']}\n"
            )
            pdf.multi_cell(0, 8, instruction)
            pdf.ln(5)
            
    return pdf.output(dest="S").encode("latin-1")

pdf_bytes = generate_pdf()
st.download_button(
    "📥 Download Improvement Guide (PDF)", 
    data=pdf_bytes, 
    file_name="EcoReceipt_Guide.pdf",
    mime="application/pdf"
)

if st.button("⬅ Upload More"):
    st.switch_page("app.py")