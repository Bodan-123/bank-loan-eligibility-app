import fitz
import re
import sqlite3
import requests


def extract_text_from_github(pdf_url):

    response = requests.get(pdf_url)

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch PDF. Status Code: {response.status_code}"
        )

    text = ""

    doc = fitz.open(
        stream=response.content,
        filetype="pdf"
    )

    for page in doc:
        text += page.get_text() + "\n"

    doc.close()

    return text


def create_table():

    conn = sqlite3.connect("bank_rules.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bank_rules(
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


def clear_rules():

    conn = sqlite3.connect("bank_rules.db")

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM bank_rules"
    )

    conn.commit()
    conn.close()


def insert_rule(
    bank_name,
    bank_type,
    min_salary,
    max_salary,
    loan_amount,
    interest_rate
):

    conn = sqlite3.connect("bank_rules.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO bank_rules
        (
            bank_name,
            bank_type,
            min_salary,
            max_salary,
            loan_amount,
            interest_rate
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            bank_name,
            bank_type,
            min_salary,
            max_salary,
            loan_amount,
            interest_rate
        )
    )

    conn.commit()
    conn.close()


def parse_report(text):

    bank_pattern = re.compile(
        r'BANK_NAME:\s*(.*?)\n'
        r'BANK_TYPE:\s*(.*?)\n'
        r'.*?ELIGIBILITY_RULES:(.*?)END_BANK',
        re.DOTALL
    )

    rule_pattern = re.compile(
        r'RULE_\d+\s+'
        r'MIN_SALARY:\s*(\d+)\s+'
        r'MAX_SALARY:\s*(UNLIMITED|\d+)\s+'
        r'MAX_LOAN_AMOUNT:\s*(\d+)\s+'
        r'INTEREST_RATE:\s*([\d.]+)'
    )

    banks = bank_pattern.findall(text)

    total_rules = 0

    for bank_name, bank_type, rules_text in banks:

        for rule in rule_pattern.findall(rules_text):

            min_salary = int(rule[0])

            if rule[1] == "UNLIMITED":
                max_salary = 999999999
            else:
                max_salary = int(rule[1])

            loan_amount = int(rule[2])

            interest_rate = float(rule[3])

            insert_rule(
                bank_name.strip(),
                bank_type.strip(),
                min_salary,
                max_salary,
                loan_amount,
                interest_rate
            )

            total_rules += 1

    print(f"Inserted {total_rules} rules successfully.")


if __name__ == "__main__":

    create_table()

    clear_rules()

    PDF_URL = (
        "https://raw.githubusercontent.com/"
        "Bodan-123/bank-loan-eligibility/main/"
        "standard_report.pdf"
    )

    text = extract_text_from_github(
        PDF_URL
    )

    parse_report(text)

    print("GitHub Standard Report Loaded Successfully")