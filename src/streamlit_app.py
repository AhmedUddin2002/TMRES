import streamlit as st
import pandas as pd
import os
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import matplotlib.pyplot as plt
import seaborn as sns
import io
import re
st.set_page_config(layout="centered", page_title="Excel Data Cleaner")

st.title("Excel Data Cleaner and Processor")
st.markdown("Upload your Excel file (`.xlsx`), and I'll clean and process the admission data for you.")

uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    st.info("Processing your data...")

    try:
        # Read the Excel file into a DataFrame
        # skiprows=5 is used to align with the data starting from the 6th row (0-indexed)
        df_raw_uploaded = pd.read_excel(uploaded_file, skiprows=5)

        # Process the data using the defined function
        df_cleaned = clean_admission_data(df_raw_uploaded)

        st.success("Data processed successfully!")

        st.subheader("Preview of Cleaned Data:")
        st.dataframe(df_cleaned.head()) # Display first few rows

        # Provide download option for the cleaned CSV
        csv_buffer = io.StringIO()
        df_cleaned.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download Cleaned Data as CSV",
            data=csv_buffer.getvalue(),
            file_name="Cleaned_Admission_Data.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"An error occurred during processing: {e}")
        st.warning("Please ensure your Excel file has the expected structure, especially the header rows and column count.")
        st.expander("Click to see error details").exception(e)

else:
    st.info("Please upload an Excel file to get started.")
    st.markdown("""
    **Expected Excel File Structure:**
    Your Excel file should have introductory rows, and the actual data (starting with 'S.No', 'District', etc.) should begin from the **6th row** (row index 5 if 0-indexed).
    """)
