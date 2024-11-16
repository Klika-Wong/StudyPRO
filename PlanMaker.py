from fetchdb import fetch_records
import streamlit as st

from email import base64mime
import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
from openai import OpenAI
import base64
import openai
load_dotenv()

client = OpenAI(api_key = os.environ.get('OPENAI_API_KEY'))
import QuestionSolver
import PlanMaker
#streamlit run page_2.py
# 使用侧边栏选择页面

st.title("PlanMaker")


# 如果用户输入了 ID，则显示输入的内容
 
# 设置 Streamlit 页面标题




####################
# 导入 fetchdb.py 中的 fetch_records 函数
from fetchdb import fetch_records

# 设置用户ID
user_id = st.session_state.get("user_id", None)  # 要匹配的 user_id 值

# 调用 fetch_records 函数并获取结果，指定数据库和表
results_up = fetch_records(user_id)
####################


sp_input=st.chat_input("Enter the study plan you want for the period of time ")
if sp_input:
    sp_response = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages = [
            {"role":"system","content":"You are the best all-round professor in the world. Then, you will develop a detailed and thorough learning plan for the user based on their input requirements (a period of time+specific events). Here is his recent study plan:{results_up} (please ignore if not)."},
            {"role":"user","content":sp_input},
        ],
        temperature = 0.2,
            max_tokens = 500,
            n = 1
    )
    st.write(f"Student: {sp_input}")
    st.write(sp_response.choices[0].message.content) 

    
