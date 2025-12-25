import streamlit as st
from db.queries import fetch_all_employees
import pandas as pd

data = fetch_all_employees()

st.header("Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Employees", len(data))
col2.metric("Departments", len(set([d[2] for d in data])))
col3.metric("Avg Salary", 0 if len(data) <= 0 else round(sum(d[3] for d in data)/len(data), 2))

st.title("Employees Table")
st.dataframe(data, use_container_width=True)
