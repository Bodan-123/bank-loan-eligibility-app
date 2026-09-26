import sqlite3

conn = sqlite3.connect("bank_rules.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bank_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bank_name TEXT,
    bank_type TEXT,
    min_salary INTEGER,
    max_salary INTEGER,
    loan_amount INTEGER,
    interest_rate REAL
)
""")

conn.commit()
conn.close()

print("Database created successfully.")