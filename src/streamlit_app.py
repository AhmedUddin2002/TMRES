import streamlit as st
import pandas as pd

st.title("Excel File Uploaderrr")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(uploaded_file)
        st.success("File uploaded and read successfully!")
        st.dataframe(df) # Display the DataFrame for verification

    except Exception as e:
        st.error(f"An error occurred while reading the Excel file: {e}")
        st.stop() # Stop execution if an error occurs
else:
    st.info("Please upload an Excel file to proceed.")