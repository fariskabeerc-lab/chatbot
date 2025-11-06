import streamlit as st
import pandas as pd
import openai

# --- CONFIG ---
st.set_page_config(page_title="📊 Sales Data Chatbot", layout="wide")
st.title("💬 Sales & Inventory Chatbot")

# Load API key
openai.api_key = st.secrets["openai"]["api_key"]

# --- LOAD DATA ---
@st.cache_data
def load_excel_data():
    df1 = pd.read_excel("SAM_Stock Comparison.Xlsx")
    df2 = pd.read_excel("SAO_Stock Comparison.Xlsx")
    df3 = pd.read_excel("SBM_Stock Comparison.Xlsx")
    df = pd.concat([df1, df2, df3], ignore_index=True)
    return df

data = load_excel_data()

st.success("✅ Excel data loaded successfully!")
with st.expander("📂 View first few rows of data"):
    st.dataframe(data.head(10))

# --- CHAT SECTION ---
st.subheader("Ask questions about your data 👇")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
user_query = st.chat_input("Type your question...")

if user_query:
    st.chat_message("user").write(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Prepare context for ChatGPT
    summary = data.head(10).to_string(index=False)
    prompt = f"""
    You are a data analyst. You have access to sales and inventory data with columns:
    Category, Barcode, Item Name, Item No, CF, Unit, Cost Price, Book Stock, Phys Stock, Diff Stock, Book Value, Phys Value, Diff Value.

    A sample of the data is shown below:
    {summary}

    The user asked: {user_query}
    Analyze or estimate the answer based on this kind of data and explain clearly.
    """

    with st.spinner("Analyzing data..."):
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful sales analyst."},
                {"role": "user", "content": prompt}
            ]
        )

    answer = response["choices"][0]["message"]["content"]
    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
