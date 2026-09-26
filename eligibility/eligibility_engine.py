import sqlite3


import sqlite3


def load_rules():

    conn = sqlite3.connect("bank_rules.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            bank_name,
            bank_type,
            min_salary,
            max_salary,
            loan_amount,
            interest_rate
        FROM bank_rules
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def check_eligibility(user_data):

    salary = user_data["salary"]

    rows = load_rules()

    eligible_banks = []

    for row in rows:

        (
            bank_name,
            bank_type,
            min_salary,
            max_salary,
            loan_amount,
            interest_rate
        ) = row

        if min_salary <= salary <= max_salary:

            eligible_banks.append({
                "bank": bank_name,
                "bank_type": bank_type,
                "loan_amount": loan_amount,
                "interest_rate": interest_rate
            })

    return eligible_banks

def get_recommendations(results):

    if not results:
        return None, None

    best_loan = max(
        results,
        key=lambda x: x["loan_amount"]
    )

    lowest_interest = min(
        results,
        key=lambda x: x["interest_rate"]
    )

    return best_loan, lowest_interest


if __name__ == "__main__":

    user_data = {
        "name": "Rahul Kumar",
        "salary": 700000,
        "company": "TCS"
    }

    results = check_eligibility(user_data)

    if not results:
        print("No eligible banks found.")
    else:

        print("\nEligible Banks:\n")

        for bank in results:

            print(
                f"{bank['bank']} | "
                f"Loan Amount: ₹{bank['loan_amount']:,} | "
                f"Interest Rate: {bank['interest_rate']}%"
            )

        best_loan, lowest_interest = get_recommendations(results)

        print("\nBest Loan Offer:")
        print(best_loan)

        print("\nLowest Interest Rate:")
        print(lowest_interest)