import streamlit as st
import pandas as pd
from openai import OpenAI

# --- Initialize OpenAI ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="📦 Stock Comparison Chatbot", layout="wide")
st.title("📦 Stock Comparison Chatbot")

# --- Load and cache Excel data ---
@st.cache_data
def load_excel_data():
    df1 = pd.read_excel("data/SAM_Stock Comparison.Xlsx")
    df2 = pd.read_excel("data/SAO_Stock Comparison.Xlsx")
    df3 = pd.read_excel("data/SBM_Stock Comparison.Xlsx")
    df = pd.concat([df1, df2, df3], ignore_index=True)
    
    # Calculate totals automatically
    df["Total Book Stock"] = df["Book Stock"].sum()
    df["Total Physical Stock"] = df["Phys Stock"].sum()
    df["Total Diff Stock"] = df["Diff Stock"].sum()
    
    df["Total Book Value"] = df["Book Value"].sum()
    df["Total Phys Value"] = df["Phys Value"].sum()
    df["Total Diff Value"] = df["Diff Value"].sum()
    
    return df

df = load_excel_data()

# --- Show data preview ---
with st.expander("🧾 Preview Combined Data"):
    st.dataframe(df.head(15))

# --- Chatbot ---
st.subheader("💬 Ask questions about your stock data")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Type your question here...")

if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare context for GPT
    # Include calculated totals for better answers
    context = f"""
    You are a data analyst assistant.
    
    The user has stock comparison data with columns:
    {', '.join(df.columns)}

    Key Totals:
    Total Book Stock: {df['Book Stock'].sum()}
    Total Physical Stock: {df['Phys Stock'].sum()}
    Total Diff Stock: {df['Diff Stock'].sum()}
    Total Book Value: {df['Book Value'].sum()}
    Total Physical Value: {df['Phys Value'].sum()}
    Total Diff Value: {df['Diff Value'].sum()}

    Here are the first 10 rows for context:
    {df.head(10).to_string(index=False)}

    Answer the user's question clearly and refer to the data.
    User question: {user_input}
    """

    # Call OpenAI GPT (new API)
    response = client.responses.create(
        model="gpt-4o-mini",
        input=context
    )

    answer = response.output_text
    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
