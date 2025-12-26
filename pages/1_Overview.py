import streamlit as st
from db.queries import (
    fetch_employees_with_departments,
    fetch_departments_stats,
    fetch_projects,
    fetch_project_employee_counts,
    fetch_employee_project_assignments
)

employees = fetch_employees_with_departments()
departments = fetch_departments_stats()
projects = fetch_projects()
assignments = fetch_employee_project_assignments()

employees = employees.set_index("id")
departments = departments.set_index("id")
projects = projects.set_index("id")

st.title("Overview")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Employees", "Departments", "Projects", "Assignments"]
)

with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Employees", len(employees))
    col2.metric(
        "Newest Hire",
        employees['hire_date'].max()
    )
    col3.metric("Avg Salary", f"{employees['salary'].mean():,.2f} MAD")

    st.subheader("Employees Overview")
    st.dataframe(employees, use_container_width=True)

with tab2:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Departments", departments.shape[0])
    col2.metric("Total Employees", departments['employee_count'].sum())
    col3.metric(
        "Avg Dept Salary",
        f"{departments['avg_salary'].mean():,.2f} MAD"
    )

    st.subheader("Departments Overview")
    st.dataframe(departments, use_container_width=True)

with tab3:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Projects", len(projects))
    col2.metric("Avg Budget", f"{projects['budget'].mean():,} MAD")
    col3.metric("Total Budget", f"{projects['budget'].sum():,} MAD")

    st.subheader("Projcets Overview")
    st.dataframe(projects, use_container_width=True)

with tab4:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Assignments", len(assignments))
    assignments["employee_fullname"] = assignments["employee_firstname"] + " " + assignments["employee_lastname"]
    col2.metric("Employees on Projects", assignments["employee_fullname"].nunique())
    col3.metric("Projects Assigned", assignments["project"].nunique())


    st.subheader("Assignments Overview")
    st.dataframe(assignments, use_container_width=True)
