import streamlit as st
import pandas as pd
import plotly.express as px
from db.queries import (
    fetch_employees_with_departments,
    fetch_departments_stats,
    fetch_projects,
    fetch_employee_project_assignments,
    fetch_project_employee_counts,
)

# Page configuration
st.set_page_config(page_title="Analytics Dashboard", layout="wide")

st.title("Analytics Dashboard")
st.markdown("---")

# --- Load Data ---
try:
    employees_df = fetch_employees_with_departments()
    departments_stats_df = fetch_departments_stats()
    projects_df = fetch_projects()
    assignments_df = fetch_employee_project_assignments()
    project_counts_df = fetch_project_employee_counts()
except Exception as e:
    st.error(f"An error occurred while fetching data: {e}")
    st.stop() # Stop execution if data cannot be loaded

# --- Top-Level Metrics ---
st.header("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Employees", f"{employees_df.shape[0]:,}")
with col2:
    st.metric("Total Departments", f"{departments_stats_df.shape[0]:,}")
with col3:
    st.metric("Total Projects", f"{projects_df.shape[0]:,}")
with col4:
    st.metric("Total Assignments", f"{assignments_df.shape[0]:,}")

st.markdown("---")

# --- Charts and Tables ---
col1, col2 = st.columns(2)

with col1:
    # --- Department Analytics ---
    st.subheader("Department Insights")
    if not departments_stats_df.empty:
        # Bar Chart: Number of employees per department
        fig_employees_per_dept = px.bar(
            departments_stats_df,
            x="department",
            y="employee_count",
            title="Number of Employees per Department",
            labels={"department": "Department", "employee_count": "Number of Employees"},
            color="department",
        )
        st.plotly_chart(fig_employees_per_dept, use_container_width=True)
        
        # Display department stats table
        with st.expander("View Department Data"):
            st.dataframe(departments_stats_df.set_index("department"), use_container_width=True)
    else:
        st.warning("No department data to display.")

    # --- Employee Analytics ---
    st.subheader("Employee Salary Distribution")
    if not employees_df.empty:
        # Histogram: Salary distribution
        fig_salary_dist = px.histogram(
            employees_df,
            x="salary",
            nbins=20,
            title="Employee Salary Distribution",
            labels={"salary": "Salary Range", "count": "Number of Employees"},
            color_discrete_sequence=['skyblue']
        )
        st.plotly_chart(fig_salary_dist, use_container_width=True)
        
        with st.expander("View Employee Data"):
            st.dataframe(employees_df.set_index("id"), use_container_width=True)
    else:
        st.warning("No employee data to display.")


with col2:
    # --- Project Analytics ---
    st.subheader("Project Insights")
    if not project_counts_df.empty:
        # Pie Chart: Employee distribution across projects
        fig_project_employees = px.pie(
            project_counts_df,
            names="project",
            values="employee_count",
            title="Employee Distribution Across Projects",
            hole=0.3,
        )
        st.plotly_chart(fig_project_employees, use_container_width=True)
        
        with st.expander("View Project Data"):
            st.dataframe(projects_df.set_index("id"), use_container_width=True)
    else:
        st.warning("No project data to display.")
        
    # --- Assignments Analytics ---
    st.subheader("Employee Project Load")
    if not assignments_df.empty:
        # Count projects per employee
        employee_load = assignments_df.groupby(["employee_firstname", "employee_lastname"]).size().reset_index(name='project_count')
        employee_load['full_name'] = employee_load['employee_firstname'] + ' ' + employee_load['employee_lastname']
        
        # Bar Chart: Number of projects per employee
        fig_employee_load = px.bar(
            employee_load.sort_values('project_count', ascending=False),
            x="full_name",
            y="project_count",
            title="Number of Projects per Employee",
            labels={"full_name": "Employee", "project_count": "Number of Projects"},
            color="project_count",
            color_continuous_scale=px.colors.sequential.Viridis,
        )
        st.plotly_chart(fig_employee_load, use_container_width=True)
        
        with st.expander("View Assignments Data"):
            st.dataframe(assignments_df, use_container_width=True)
    else:
        st.warning("No assignment data to display.")

st.markdown("---")