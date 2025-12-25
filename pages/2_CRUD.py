import streamlit as st
from db.connection import get_connection

st.header("CRUD Operations")

with st.form("add_employee"):
    name = st.text_input("Name")
    dept = st.selectbox("Department", ["IT", "HR", "Finance"])
    salary = st.number_input("Salary", 0.0)
    submitted = st.form_submit_button("Add")

    if submitted:
        conn = get_connection()
        conn.execute(
            "INSERT INTO employees(name, department, salary) VALUES (?, ?, ?)",
            (name, dept, salary)
        )
        conn.commit()
        st.success("Employee added")
