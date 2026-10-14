import mysql.connector
import streamlit as st
from dotenv import load_dotenv

from auth import authenticate_user, register_user

load_dotenv()
st.title("StudyPRO")

if not st.session_state.get("authenticated"):
    login_tab, register_tab = st.tabs(["Log in", "Create account"])

    with login_tab:
        with st.form("login_form"):
            login_id = st.text_input("User ID", max_chars=10)
            login_password = st.text_input("Password", type="password")
            login_submitted = st.form_submit_button("Log in")

        if login_submitted:
            try:
                if authenticate_user(login_id, login_password):
                    st.session_state.authenticated = True
                    st.session_state.user_id = login_id.strip()
                    st.rerun()
                st.error("User ID or password is incorrect.")
            except (RuntimeError, ValueError) as exc:
                st.error(str(exc))
            except mysql.connector.Error:
                st.error("Unable to access the user database. Check its setup and connection.")

    with register_tab:
        with st.form("register_form"):
            new_id = st.text_input("Choose a user ID (up to 10 letters or numbers)", max_chars=10)
            new_password = st.text_input("Choose a password (at least 10 characters)", type="password")
            confirm_password = st.text_input("Confirm password", type="password")
            register_submitted = st.form_submit_button("Create account")

        if register_submitted:
            if new_password != confirm_password:
                st.error("The passwords do not match.")
            else:
                try:
                    register_user(new_id, new_password)
                    st.success("Account created. Log in to continue.")
                except (RuntimeError, ValueError) as exc:
                    st.error(str(exc))
                except mysql.connector.Error:
                    st.error("Unable to access the user database. Check its setup and connection.")
    st.stop()

st.write(f"Signed in as {st.session_state.user_id}")
if st.button("Log out"):
    st.session_state.clear()
    st.rerun()

pg = st.navigation([
    st.Page("QuestionSolver.py", title="Question Solver"),
    st.Page("PlanMaker.py", title="Study Plan"),
    st.Page("04.py", title="Study Progress"),
])
pg.run()
