import sqlite3
import random
from datetime import date, timedelta

DB_PATH = "database.db"

NAMES = [
    "Ahmed", "Sara", "Youssef", "Imane", "Omar",
    "Khadija", "Yassine", "Salma", "Anas", "Noura"
]

DEPARTMENTS = ["IT", "HR", "Finance", "Marketing", "Sales"]

def random_date(start_year=2018):
    start = date(start_year, 1, 1)
    end = date.today()
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create the first table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary REAL NOT NULL,
    hire_date TEXT NOT NULL
)
""")

# Delete Old data
cursor.execute("DELETE FROM employees")

# Insert New one
for _ in range(50):
    cursor.execute("""
        INSERT INTO employees (name, department, salary, hire_date)
        VALUES (?, ?, ?, ?)
    """, (
        random.choice(NAMES),
        random.choice(DEPARTMENTS),
        round(random.uniform(4000, 20000), 2),
        random_date().isoformat()
    ))

conn.commit()
conn.close()
