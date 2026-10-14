
 ##streamlit run QuestionSolver.py  
import insert_questions as insert_questions  # 导入 insert_questions 模块
import json

from email import base64mime
import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
from openai import OpenAI
import base64
import openai
load_dotenv()

if not st.session_state.get("authenticated"):
    st.info("Log in from the StudyPRO navigation page to continue.")
    st.stop()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
import streamlit as st
from io import BytesIO

# 设置 Streamlit 页面标题
def save_question_response(raw_response):
    try:
        question_data = json.loads(raw_response)
    except (TypeError, json.JSONDecodeError) as exc:
        st.error("The generated question data was not valid JSON; nothing was saved.")
        return

    if not isinstance(question_data, dict):
        st.error("The generated question data had an unexpected format; nothing was saved.")
        return

    required_fields = {
        "question_text",
        "question_type",
        "question_options",
        "correct_answer",
        "difficulty_level",
        "subjects",
    }
    if not required_fields.issubset(question_data):
        st.error("The generated question data was incomplete; nothing was saved.")
        return

    user_id = st.session_state.get("user_id")
    if user_id is None:
        st.error("Enter your user ID before saving a question.")
        return

    try:
        insert_questions.insert_question(
            question_data=question_data,
            user_id=user_id,
            database="questionbank",
        )
    except (ValueError, RuntimeError) as exc:
        st.error(str(exc))


st.title("QuestionSolver")
#type question
user_input = st.chat_input("Type your question ")

if user_input:
    response = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages = [
            {"role":"system","content":"You are the world's top general professor. You need to analyze the questions which user inputs. If the question already has an answer, you need to analyze whether the answer is correct. If there is no answer, please provide an analysis of the answer."},
            {"role":"user","content":user_input}
        ],
        temperature = 0.2,
        max_tokens = 500,
        n = 1,
    )
    st.write(f"Student: {user_input}")

    st.write(response.choices[0].message.content)
  
    
    ai_output = response.choices[0].message.content
    response2 = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages = [
            {"role":"system","content":"""Please integrate the input content into a form that can be imported into the database as strict JSON. Return only the JSON object, with no Markdown or extra prose. And language use same. The format is as follows:
            {
            "question_text": "What is the capital of France?",
            "question_type": "Multiple Choice",
            "question_options": {"A": "Paris", "B": "Berlin", "C": "Madrid", "D": "Rome"},
            "correct_answer": "A",
            "difficulty_level": 2,
            "subjects": "Geography"
            }"""},
            {"role":"user","content":ai_output}
        ],
        temperature = 0.2,
        max_tokens = 500,
        n = 1,
    )    
    

    sql_info = response2.choices[0].message.content
    
    save_question_response(sql_info)
    
    
    
    
#Image uploading
st.title("upload your question image")

uploaded_file = st.file_uploader("please choice a image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:

    image = Image.open(uploaded_file)
    
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    if image.mode == "RGBA":
        image = image.convert("RGB")
    buffered = BytesIO()
    image.save(buffered, format="JPEG")  
    img_bytes = buffered.getvalue()  
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")


    response = client.chat.completions.create(
                model = 'gpt-4o-mini',
                messages = [
                    {
                        "role":"user",
                        "content":[
                            {"type" : "text", 
                            "text" : "You are the world's top general doctor. You need to analyze the questions in the picture. If the question already has an answer, you need to analyze whether the answer is correct. If there is no answer, please provide an analysis of the answer.",
                            },
                            {
                                "type":"image_url",
                                "image_url" : {
                                    
                                    "url": f"data:image/jpeg;base64,{img_base64}"
                                }
                            }
                        ]
                    }
                ]
            )
    st.write(response.choices[0].message.content)
    
    
    ai_output = response.choices[0].message.content
    response3 = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages = [
            {"role":"system","content":"""Please integrate the input content into a form that can be imported into the database as strict JSON. Return only the JSON object, with no Markdown or extra prose. And language use same. The format is as follows:
            {
            "question_text": "What is the capital of France?",
            "question_type": "Multiple Choice",
            "question_options": {"A": "Paris", "B": "Berlin", "C": "Madrid", "D": "Rome"},
            "correct_answer": "A",
            "difficulty_level": 2,
            "subjects": "Geography"
            }"""},
            {"role":"user","content":ai_output}
        ],
        temperature = 0.2,
        max_tokens = 500,
        n = 1,
    )    
    

    sql_info = response3.choices[0].message.content
    
    save_question_response(sql_info)
    










# Using object notation
add_selectbox = st.sidebar.selectbox(
    "what object you want to ask?",
    ("English", "History", "Math","programme")
)

# Using "with" notation
with st.sidebar:
     add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
