import streamlit as st

st.set_page_config(page_title="EcoReceipt", layout="centered")

st.title("🌍 EcoReceipt")
st.markdown("### Small shopping choices. Big environmental impact.")

st.markdown("""
Upload your receipt images (JPG / PNG only) and discover:

• Your environmental impact score  
• Areas to improve  
• Greener alternatives  
""")

uploaded_files = st.file_uploader(
    "Upload Receipt Images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    st.session_state["uploaded_files"] = uploaded_files

    if st.button("Analyze Receipts"):
        st.switch_page("pages/1_Report.py")
