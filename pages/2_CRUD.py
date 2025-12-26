import streamlit as st
import pandas as pd
from db.queries import (
    fetch_employees_with_departments,
    fetch_all_departments,
    fetch_employee_by_id,
    add_employee,
    update_employee,
    delete_employee,
)

st.set_page_config(page_title="Employee Management", layout="wide")

st.title("Employee Management")

employees_df = fetch_employees_with_departments()
departments_df = fetch_all_departments()
department_map = departments_df.set_index("id")["name"].to_dict()

tab1, tab2, tab3 = st.tabs(["Add Employee", "Update Employee", "Delete Employee"])

with tab1:
    st.header("Add a New Employee")
    with st.form("add_employee_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            fname = st.text_input("First Name", placeholder="e.g., John")
            department_id = st.selectbox(
                "Department",
                options=departments_df["id"],
                format_func=lambda x: department_map[x],
            )
        with col2:
            lname = st.text_input("Last Name", placeholder="e.g., Doe")
            salary = st.number_input(
                "Salary", min_value=0.0, step=500.0, value=3000.0, format="%.2f"
            )

        submitted = st.form_submit_button("Add Employee")
        if submitted:
            if not fname or not lname:
                st.warning("First name and last name are required.")
            else:
                try:
                    add_employee(fname, lname, department_id, salary)
                    st.success("Employee added successfully!")
                except Exception as e:
                    st.error(f"Error adding employee: {e}")

with tab2:
    st.header("Update an Existing Employee")

    # Dropdown to select an employee
    employee_list = employees_df.apply(
        lambda row: f"{row['fname']} {row['lname']} (ID: {row['id']})", axis=1
    ).tolist()

    if not employee_list:
        st.warning("No employees found. Please add an employee first.")
    else:
        selected_employee_str = st.selectbox(
            "Select Employee to Update", options=employee_list
        )

        # Extract ID from the selected string
        employee_id_to_update = int(selected_employee_str.split(" (ID: ")[1][:-1])

        # Fetch the selected employee's current data
        employee_data = fetch_employee_by_id(employee_id_to_update)

        if not employee_data.empty:
            current_employee = employee_data.iloc[0]

            with st.form("update_employee_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_fname = st.text_input(
                        "First Name", value=current_employee["fname"]
                    )
                    # Get the index of the current department for the selectbox
                    dept_ids = list(department_map.keys())
                    current_dept_index = dept_ids.index(
                        current_employee["department_id"]
                    )
                    new_department_id = st.selectbox(
                        "Department",
                        options=dept_ids,
                        index=current_dept_index,
                        format_func=lambda x: department_map[x],
                    )
                with col2:
                    new_lname = st.text_input(
                        "Last Name", value=current_employee["lname"]
                    )
                    new_salary = st.number_input(
                        "Salary",
                        min_value=0.0,
                        step=500.0,
                        value=3000.0,
                        format="%.2f",
                    )

                update_submitted = st.form_submit_button("Update Employee")
                if update_submitted:
                    try:
                        update_employee(
                            employee_id_to_update,
                            new_fname,
                            new_lname,
                            new_department_id,
                            new_salary,
                        )
                        st.success(
                            f"Employee ID {employee_id_to_update} updated successfully!"
                        )
                    except Exception as e:
                        st.error(f"Error updating employee: {e}")
        else:
            st.error("Could not fetch details for the selected employee.")

with tab3:
    st.header("Delete an Employee")

    if not employee_list:
        st.warning("No employees to delete.")
    else:
        # Re-using the employee list from the update tab
        employee_to_delete_str = st.selectbox(
            "Select Employee to Delete", options=employee_list, key="delete_select"
        )

        # Extract ID
        employee_id_to_delete = int(employee_to_delete_str.split(" (ID: ")[1][:-1])

        if st.button("Delete Employee", type="primary"):
            try:
                delete_employee(employee_id_to_delete)
                st.success(f"Employee ID {employee_id_to_delete} deleted successfully!")
                # To see the change, we might need to rerun the script
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error deleting employee: {e}")

st.markdown("---")
st.subheader("Current Employees")

try:
    refreshed_employees_df = fetch_employees_with_departments().set_index("id")
    st.dataframe(refreshed_employees_df, use_container_width=True)
except Exception as e:
    st.error(f"Could not fetch employee data: {e}")
