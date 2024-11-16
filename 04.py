import streamlit as st
from Analyser import parse_input, generate_line_chart
import os
from fetchdb import fetch_records
import openai 
from openai import OpenAI

####################

# 设置用户ID
#user_id = st.session_state.get("user_id", None)  # 要匹配的 user_id 值
user_id =1

# 调用 fetch_records 函数并获取结果，指定数据库和表
results_up = fetch_records(user_id)
####################


client = OpenAI(api_key = os.environ.get('OPENAI_API_KEY'))



if st.button("Generate predictive analysis chart"):
    
    
        if not hasattr(st.session_state, 'api_called') or not st.session_state.api_called:
            st.session_state.api_called = True  
        response5 = client.chat.completions.create(
            model = 'gpt-4o-mini',
            messages = [
                {"role":"system","content":""" Please integrate the input content into a form that can be imported into the database 
                 (Python dictionary).Don't mention any other words,but dictionary. {chat}Here is data to analysis, And language use same. 
                 The format is as follows:
                'time:1,2,3,4,5;English:10,11,12,13,14;Chinese:14,13,12,11,10;Geograph:10,12,14,16,18'"""},
                {"role":"user","content": " output data for diagrame"}
        ],
        temperature = 0.2,
        max_tokens = 500,
        n = 1,
        )    


        re = response5.choices[0].message.content



    ##############
        chart_data = parse_input(re)  
    
        if chart_data is not None:
            st.write("Parsed data:")
            st.write(chart_data)
        
        #generate chart
            generate_line_chart(chart_data)
 
    ###############


