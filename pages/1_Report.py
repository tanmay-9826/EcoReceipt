import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF
from PIL import Image
import sys
import os

# ===============================
# Fix Import Path For Streamlit Cloud
# ===============================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parser import clean_items
from core.scorer import match_products
from ocr_engine import ocr_image


st.set_page_config(page_title="Environmental Impact Dashboard", layout="wide")

st.title("📊 Environmental Impact Dashboard")

# ===============================
# Upload Section
# ===============================

uploaded_file = st.file_uploader(
    "Upload Receipt Image (JPG/PNG only)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    file_bytes = uploaded_file.read()
    file_stream = BytesIO(file_bytes)

    with st.spinner("Analyzing receipt..."):
        raw_text = ocr_image(file_stream)
        items = clean_items(raw_text)
        results = match_products(items)

    if len(results) == 0:
        st.warning("No valid products detected.")
        st.stop()

    df = pd.DataFrame(results)

    # Keep only required columns for customer
    df = df[[
        "item_detected",
        "matched_product",
        "impact_score",
        "category",
        "greener_alternative",
        "impact_reason"
    ]]

    # ===============================
    # Metrics
    # ===============================

    avg_score = round(df["impact_score"].mean(), 2)
    high_impact = df[df["impact_score"] >= 7].shape[0]

    col1, col2 = st.columns(2)
    col1.metric("Average Impact Score", f"{avg_score}/10")
    col2.metric("High Impact Items", high_impact)

    st.divider()

    # ===============================
    # Clean Structured Table
    # ===============================

    st.subheader("🛒 Purchased Items Analysis")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ===============================
    # Layout: Graph + Suggestions
    # ===============================

    col_graph, col_suggest = st.columns([1.2, 1])

    # -------- Graph --------
    with col_graph:
        st.subheader("📈 Item Impact Trend")

        fig, ax = plt.subplots(figsize=(7, 4))

        ax.plot(
            df["matched_product"],
            df["impact_score"],
            marker="o"
        )

        ax.set_xlabel("Items")
        ax.set_ylabel("Impact Score")
        ax.set_ylim(0, 10)

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        st.pyplot(fig)

    # -------- Suggestions --------
    with col_suggest:
        st.subheader("🌱 Suggested Improvements")

        for _, row in df.iterrows():
            if row["impact_score"] >= 7:
                st.markdown(f"""
                **{row['matched_product']} (Impact Score: {row['impact_score']})**

                Why it matters:  
                {row['impact_reason']}

                Suggested alternative:  
                **{row['greener_alternative']}**
                """)
                st.divider()

    # ===============================
    # PDF Generation (Instruction Style)
    # ===============================

    def generate_pdf(dataframe, average_score):
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Environmental Impact Improvement Guide", ln=True)

        pdf.ln(8)

        pdf.set_font("Arial", size=12)
        pdf.multi_cell(
            0, 8,
            "This report analyzes your purchased items and provides guidance "
            "on how to make more environmentally responsible choices."
        )

        pdf.ln(5)

        pdf.multi_cell(
            0, 8,
            f"Your average environmental impact score is {average_score}/10."
        )

        pdf.ln(8)

        for _, row in dataframe.iterrows():
            if row["impact_score"] >= 7:
                pdf.multi_cell(
                    0, 8,
                    f"You purchased {row['matched_product']} "
                    f"(Impact Score: {row['impact_score']}). "
                    f"This has higher environmental impact because "
                    f"{row['impact_reason']} "
                    f"Consider replacing it with {row['greener_alternative']}."
                )
                pdf.ln(4)

        pdf.ln(6)

        pdf.multi_cell(
            0, 8,
            "Small conscious changes in daily purchasing decisions "
            "can collectively create meaningful environmental impact."
        )

        return pdf.output(dest="S").encode("latin-1")

    pdf_bytes = generate_pdf(df, avg_score)

    st.download_button(
        label="📥 Download Improvement Guide (PDF)",
        data=pdf_bytes,
        file_name="EcoReceipt_Improvement_Guide.pdf",
        mime="application/pdf"
    )
