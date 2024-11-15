import streamlit as st

require('dotenv').config(); // 引入 dotenv 模块并加载环境变量

const mysql = require('mysql');

const connection = mysql.createConnection({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_DATABASE,
});

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




