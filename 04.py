import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from Analyser import generate_line_chart
from fetchdb import fetch_study_scores

load_dotenv()

if not st.session_state.get("authenticated"):
    st.info("Log in from the StudyPRO navigation page to continue.")
    st.stop()

st.title("Study Progress")
st.caption("This chart uses saved study records; it does not generate or predict scores.")

user_id = st.session_state.user_id
try:
    records = fetch_study_scores(user_id)
except (RuntimeError, ValueError) as exc:
    st.error(str(exc))
    st.stop()

if not records:
    st.info("No study score records are available yet.")
else:
    scores = pd.DataFrame(
        records,
        columns=["study_date", "correct_count", "total_count"],
    )
    scores["correct_count"] = pd.to_numeric(scores["correct_count"], errors="coerce").fillna(0)
    scores["total_count"] = pd.to_numeric(scores["total_count"], errors="coerce").fillna(0)
    scores = scores[scores["total_count"] > 0].copy()
    if scores.empty:
        st.info("Study records exist, but they do not contain score totals yet.")
    else:
        scores["accuracy_percent"] = (
            scores["correct_count"] / scores["total_count"] * 100
        ).clip(0, 100)
        generate_line_chart(scores)
        st.dataframe(
            scores[["study_date", "correct_count", "total_count", "accuracy_percent"]],
            hide_index=True,
            use_container_width=True,
        )
