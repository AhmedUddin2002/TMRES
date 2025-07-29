import streamlit as st
import pandas as pd
import os
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import matplotlib.pyplot as plt
import seaborn as sns
import io
# ---- SETUP ----
# Set your OpenAI API Key
os.environ["OPENAI_API_KEY"] = "your-openai-key-here"  # Replace with your key

st.set_page_config(page_title="AI Dashboard Analyzer", layout="wide")
st.title("📊 AI-Powered Natural Language Dashboard Generator")

# ---- FILE UPLOAD ----
uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    # ---- AUTO DASHBOARD ----
    st.subheader("📈 Automated Insights Dashboard")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📌 Basic Statistics**")
        st.write(df.describe(include='all'))

    with col2:
        st.markdown("**🧭 Data Info**")
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

    st.markdown("---")
    st.subheader("📊 Visualizations")

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    if len(numeric_cols) >= 2:
        st.markdown("**Correlation Heatmap**")
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    if len(numeric_cols) > 0:
        selected_col = st.selectbox("Select a numeric column to plot distribution", numeric_cols)
        fig, ax = plt.subplots()
        sns.histplot(df[selected_col], kde=True, ax=ax)
        st.pyplot(fig)

    # ---- LLM POWERED CHAT ----
    st.markdown("---")
    st.subheader("💬 Ask Questions About Your Data")

    llm = OpenAI()  # Initialized with key from env var
    sdf = SmartDataframe(df, config={"llm": llm})

    query = st.text_input("Ask a question in plain English (e.g., 'What are top 5 products by sales?')")

    if query:
        with st.spinner("Thinking..."):
            try:
                response = sdf.chat(query)
                st.success("Answer:")
                st.write(response)
            except Exception as e:
                st.error(f"Error: {e}")
