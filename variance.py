import streamlit as st
import pandas as pd
from openai import OpenAI

# Initialize OpenAI client using Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📦 Stock Comparison Chatbot")

# --- Load and cache Excel data ---
@st.cache_data
def load_excel_data():
    df1 = pd.read_excel("SAM_Stock Comparison.xlsx")
    df2 = pd.read_excel("SAO_Stock Comparison.xlsx")
    df3 = pd.read_excel("SBM_Stock Comparison.xlsx")
    df = pd.concat([df1, df2, df3], ignore_index=True)
    return df

df = load_excel_data()

st.write("### 🧾 Combined Data Preview")
st.dataframe(df.head())

# --- Chatbot Interface ---
user_input = st.text_input("💬 Ask a question about your stock data:")

if user_input:
    # Give GPT some data context
    context = f"""
    You are a data analyst assistant. The user has stock comparison data
    with columns: {', '.join(df.columns)}.

    Here are the first 10 rows for context:
    {df.head(10).to_string(index=False)}

    Now answer this question based on the data:
    {user_input}
    """

    # Call the GPT model using the new API
    response = client.responses.create(
        model="gpt-4o-mini",
        input=context,
    )

    # Show GPT's response
    st.write("### 🤖 Chatbot Response:")
    st.write(response.output_text)
