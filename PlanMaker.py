import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

if not st.session_state.get("authenticated"):
    st.info("Log in from the StudyPRO navigation page to continue.")
    st.stop()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
st.title("PlanMaker")
st.caption("Your study history stays in the database and is not included in the API request.")

sp_input = st.chat_input("Enter the study plan you want for the period of time")
if sp_input:
    sp_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Create a detailed learning plan based on the user's request.",
            },
            {"role": "user", "content": sp_input},
        ],
        temperature=0.2,
        max_tokens=500,
    )
    st.write(sp_response.choices[0].message.content)
