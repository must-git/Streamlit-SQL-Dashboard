import sqlite3
import random
from datetime import date, timedelta

DB_PATH = "database.db"

FNAMES = [
    "Ahmed",
    "Sara",
    "Youssef",
    "Imane",
    "Omar",
    "Khadija",
    "Yassine",
    "Salma",
    "Anas",
    "Noura",
]

LNAMES = [
    "El Amrani",
    "Benali",
    "El Idrissi",
    "Alaoui",
    "Bennani",
    "El Fassi",
    "Chakiri",
    "Zerouali",
    "Touhami",
    "Lahlou",
    "Belkadi",
    "Amine",
    "Mouline",
    "Sbai",
    "Haddad",
]

DEPARTMENTS = ["IT", "HR", "Finance", "Marketing", "Sales"]

PROJECTS = [
    "ERP System",
    "Website Redesign",
    "Mobile App",
    "Marketing Campaign",
    "Data Warehouse",
]

ROLES = ["Developer", "Analyst", "Manager", "Tester"]

def random_date(start_year=2018):
    start = date(start_year, 1, 1)
    end = date.today()
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

cursor.executescript(
    """
DROP TABLE IF EXISTS employee_projects;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    fname TEXT NOT NULL,
    lname TEXT NOT NULL,
    department_id INTEGER,
    salary REAL NOT NULL,
    hire_date TEXT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    budget REAL NOT NULL,
    start_date TEXT NOT NULL
);

CREATE TABLE employee_projects (
    employee_id INTEGER,
    project_id INTEGER,
    role TEXT,
    PRIMARY KEY (employee_id, project_id),
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
"""
)

# Departments
for d in DEPARTMENTS:
    cursor.execute("INSERT INTO departments (name) VALUES (?)", (d,))

# Employees
dates = [random_date() for _ in range(50)]
dates.sort()

for hire_date in dates:
    cursor.execute(
        """
        INSERT INTO employees (fname, lname, department_id, salary, hire_date)
        VALUES (?, ?, ?, ?, ?)
    """,
        (
            random.choice(FNAMES),
            random.choice(LNAMES),
            random.randint(1, len(DEPARTMENTS)),
            round(random.uniform(4000, 20000)),
            hire_date.isoformat(),
        ),
    )

# Projects
for p in PROJECTS:
    cursor.execute(
        """
        INSERT INTO projects (name, budget, start_date)
        VALUES (?, ?, ?)
    """,
        (p, round(random.uniform(50000, 300000)), random_date(2020).isoformat()),
    )

# Employee ↔ Project assignments
for emp_id in range(1, 51):
    for proj_id in random.sample(range(1, len(PROJECTS) + 1), k=2):
        cursor.execute(
            """
            INSERT INTO employee_projects (employee_id, project_id, role)
            VALUES (?, ?, ?)
        """,
            (emp_id, proj_id, random.choice(ROLES)),
        )

conn.commit()
conn.close()

print("Database seeded successfully.")
