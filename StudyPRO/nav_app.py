import streamlit as st


st.image("./logo.png", width=100)
st.title("enter id")
user_id = st.text_input("user ID:")
if user_id:
    st.write(f"ID is: {user_id}")
    st.session_state.user_id = user_id
    
pg = st.navigation([st.Page("QuestionSolver.py"), st.Page("PlanMaker.py")])
pg.run()




