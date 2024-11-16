import streamlit as st
import pandas as pd
import plotly.express as px


# define parse_input function,use to expalian chart

def parse_input(question_input):
    """
    
    输入格式：'time:1,2,3,4,5;test1:10,11,12,13,14;test2:14,13,12,11,10;test3:10,12,14,16,18'
    
    """
    data = {}
    subjects = question_input.split(";")
    
    for i, subject in enumerate(subjects):
            if i >= 10:  
                break
            
            if ":" in subject:
                key, values = subject.split(":")
                data[key.strip()] = list(map(int, values.split(",")))
                
        
    # return DataFrame
    return pd.DataFrame(data)



# define generate_line_chart ，chart
def generate_line_chart(data):
    """
    根据 DataFrame function create a diagram
    """
    'time' not in data.columns
    
    fig = px.line(
        data,
        x='time',
        y=data.columns[1:],  # 绘制除 'time' 列以外的其他列
        title='Summary Line Chart'
    )
    
    # 添加 y 轴和 x 轴标签
    fig.update_layout(
        xaxis_title="time",
        yaxis_title="level"
    )
    
    st.plotly_chart(fig)