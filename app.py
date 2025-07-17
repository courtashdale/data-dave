# https://www.youtube.com/watch?v=oSC2U2iuMRg
# Pandas AI: https://github.com/sinaptik-ai/pandas-ai
# Streamlit Docs: https://docs.streamlit.io/develop/api-reference/chat/st.chat_input

# app.py

from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI

# Load API key
load_dotenv()
API_KEY = os.environ.get("OPENAI_API_KEY")

if not API_KEY:
    st.error("OPENAI_API_KEY not found. Please check your .env file.")
    st.stop()

# Set up LLM
llm = OpenAI(api_token=API_KEY)

st.title("🤖 Data Dave")
st.subheader("Prompt-driven data analysis")

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Read file based on type
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type.")
            st.stop()

        st.write("📊 Data Preview:")
        st.dataframe(df.head(5))

        # Initialize SmartDataframe
        sdf = SmartDataframe(df, config={"llm": llm})

        # Chat input box (uses Enter to submit)
        user_prompt = st.chat_input("Ask Dave...")

        if user_prompt:
            with st.spinner("🧠 Data Dave is thinking..."):
                try:
                    result = sdf.chat(user_prompt)
                    st.success("✅ Here's the result:")
                    st.write(result)
                except Exception as e:
                    st.error(f"❌ Error processing your request: {e}")
    except Exception as e:
        st.error(f"⚠️ Failed to load file: {e}")