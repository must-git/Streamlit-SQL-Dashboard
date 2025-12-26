import streamlit as st
from db.connection import get_connection
from db.seed import DEPARTMENTS as deps
from datetime import date

st.header("CRUD Operations")

with st.form("add_employee"):
    name = st.text_input("Name")
    dept = st.selectbox("Department", deps)
    salary = st.number_input("Salary", 0.0)
    submitted = st.form_submit_button("Add")

    if submitted:
        conn = get_connection()
        conn.execute(
            "INSERT INTO employees(name, department, salary, hire_date) VALUES (?, ?, ?, ?)",
            (name, dept, salary, date.today())
        )
        conn.commit()
        st.success("Employee added")
