import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from fetchdb import fetch_records

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

st.title("PlanMaker")

user_id = st.session_state.get("user_id")
if user_id is None:
    st.info("Enter your user ID from the navigation page first.")
else:
    results = fetch_records(user_id)
    sp_input = st.chat_input("Enter the study plan you want for the period of time")
    if sp_input:
        sp_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Create a detailed learning plan based on the user's "
                        f"requirements and recent study records: {results}"
                    ),
                },
                {"role": "user", "content": sp_input},
            ],
            temperature=0.2,
            max_tokens=500,
        )
        st.write(f"Student: {sp_input}")
        st.write(sp_response.choices[0].message.content)
