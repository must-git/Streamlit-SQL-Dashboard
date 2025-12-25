# import sqlite3
from db.queries import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("""
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        department TEXT,
        salary REAL,
        hire_date TEXT
    );
          
"""
)