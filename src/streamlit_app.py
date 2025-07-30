import streamlit as st
import pandas as pd
from clean_admission_data import clean_admission_data
import tempfile
import os

st.set_page_config(page_title="TMREIS Data Cleaner", layout="centered")

st.title("📊 TMREIS Admission Data Cleaner")
st.markdown("Upload a raw `.xlsx` admission data file, and get back a cleaned `.csv` file.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_input:
        tmp_input.write(uploaded_file.read())
        input_path = tmp_input.name

    output_path = os.path.join(tempfile.gettempdir(), "cleaned_output.csv")

    try:
        clean_admission_data(input_path, output_path)

        with open(output_path, "rb") as f:
            st.success("🎉 File cleaned successfully! Download below.")
            st.download_button(
                label="⬇️ Download Cleaned CSV",
                data=f,
                file_name="TMREIS_Cleaned_Data.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
