import streamlit as st
import os
from dotenv import load_dotenv



# 加载 .env 文件
load_dotenv()

# 获取环境变量
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_database = os.getenv("DB_DATABASE")


connection.connect((err) => {
  if (err) throw err;
  console.log("Connected to MySQL database!");
});


st.title("enter id")
user_id = st.text_input("user ID:")
if user_id:
    st.write(f"ID is: {user_id}")
    st.session_state.user_id = user_id
    
pg = st.navigation([st.Page("QuestionSolver.py"), st.Page("PlanMaker.py")])
pg.run()




