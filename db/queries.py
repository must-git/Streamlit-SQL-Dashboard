import pandas as pd
from db.connection import get_connection

def fetch_employees_with_departments():
    conn = get_connection()
    return pd.read_sql(
        """
        SELECT
            e.id,
            e.fname,
            e.lname,
            d.name AS department,
            e.salary,
            e.hire_date
        FROM employees e
        JOIN departments d ON e.department_id = d.id
    """,
        conn,
    )

def fetch_departments_stats():
    conn = get_connection()
    return pd.read_sql(
        """
        SELECT
            d.id,
            d.name AS department,
            COUNT(e.id) AS employee_count,
            ROUND(AVG(e.salary), 2) AS avg_salary
        FROM departments d
        LEFT JOIN employees e ON e.department_id = d.id
        GROUP BY d.id
    """,
        conn,
    )

def salary_by_department():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT d.name, AVG(e.salary)
        FROM departments d JOIN employees e ON e.department_id = d.id
        GROUP BY d.name
    """
    )
    return cur.fetchall()

def fetch_projects():
    conn = get_connection()
    return pd.read_sql("""
        SELECT
            id,
            name,
            budget,
            start_date
        FROM projects
        ORDER BY start_date
    """, conn)

def fetch_project_employee_counts():
    conn = get_connection()
    return pd.read_sql("""
        SELECT
            p.name AS project,
            COUNT(ep.employee_id) AS employee_count
        FROM projects p
        LEFT JOIN employee_projects ep
            ON p.id = ep.project_id
        GROUP BY p.id
        ORDER BY employee_count DESC
    """, conn)

def fetch_employee_project_assignments():
    conn = get_connection()
    return pd.read_sql("""
        SELECT
            e.fname AS employee_firstname,
            e.lname AS employee_lastname,
            d.name AS department,
            p.name AS project,
            ep.role
        FROM employee_projects ep
        JOIN employees e ON ep.employee_id = e.id
        JOIN departments d ON e.department_id = d.id
        JOIN projects p ON ep.project_id = p.id
        ORDER BY p.name, e.lname, e.fname
    """, conn)

def fetch_all_departments():
    conn = get_connection()
    return pd.read_sql("SELECT id, name FROM departments", conn)

def fetch_employee_by_id(employee_id):
    conn = get_connection()
    return pd.read_sql(f"SELECT id, fname, lname, department_id, salary FROM employees WHERE id = {employee_id}", conn)

def add_employee(fname, lname, department_id, salary):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO employees (fname, lname, department_id, salary, hire_date)
        VALUES (?, ?, ?, ?, DATE('now'))
        """,
        (fname, lname, department_id, salary),
    )
    conn.commit()

def update_employee(employee_id, fname, lname, department_id, salary):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE employees
        SET fname = ?, lname = ?, department_id = ?, salary = ?
        WHERE id = ?
        """,
        (fname, lname, department_id, salary, employee_id),
    )
    conn.commit()

def delete_employee(employee_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
    conn.commit()
