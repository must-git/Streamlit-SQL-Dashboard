from db.connection import get_connection

def fetch_all_employees():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    return cur.fetchall()

def salary_by_department():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT department, AVG(salary)
        FROM employees
        GROUP BY department
    """)
    return cur.fetchall()
