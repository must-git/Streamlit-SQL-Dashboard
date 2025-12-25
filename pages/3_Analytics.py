import streamlit as st
import pandas as pd
import plotly.express as px
from db.queries import salary_by_department

data = salary_by_department()
df = pd.DataFrame(data, columns=["Department", "Avg Salary"])

st.header("Analytics")
fig = px.bar(df, x="Department", y="Avg Salary", text_auto=True)
st.plotly_chart(fig, use_container_width=True)
