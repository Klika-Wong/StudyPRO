import plotly.express as px
import streamlit as st


def generate_line_chart(data):
    """Display daily accuracy derived from recorded study counts."""
    fig = px.line(
        data,
        x="study_date",
        y="accuracy_percent",
        markers=True,
        title="Daily study accuracy",
    )
    fig.update_layout(
        xaxis_title="Study date",
        yaxis_title="Correct answers (%)",
        yaxis_range=[0, 100],
    )
    st.plotly_chart(fig, use_container_width=True)
