import streamlit as st
import pandas as pd
import tempfile

from ingestion.user_parser import (
    extract_text,
    extract_user_details
)

from eligibility.eligibility_engine import (
    check_eligibility,
    get_recommendations
)

st.set_page_config(
    page_title="Bank Loan Eligibility Analyzer",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Bank Loan Eligibility Analyzer")

st.markdown(
    "Upload a User Loan Application Report PDF to check loan eligibility."
)

uploaded_file = st.file_uploader(
    "Upload User Report PDF",
    type=["pdf"]
)

if uploaded_file:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(uploaded_file.read())
        pdf_path = temp_file.name

    text = extract_text(pdf_path)

    user_data = extract_user_details(text)

    st.subheader("👤 Applicant Details")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Name:** {user_data['name']}")
        st.write(f"**Aadhaar:** {user_data['aadhaar']}")
        st.write(f"**PAN:** {user_data['pan']}")

    with col2:
        st.write(f"**Company:** {user_data['company']}")
        st.write(f"**Salary:** ₹{user_data['salary']:,}")

    results = check_eligibility(user_data)

    if not results:

        st.error(
            "No eligible banks found for this applicant."
        )

    else:

        st.subheader("🏦 Eligible Banks")

        df = pd.DataFrame(results)

        df["loan_amount"] = df["loan_amount"].apply(
            lambda x: f"₹{x:,}"
        )

        df["interest_rate"] = df["interest_rate"].apply(
            lambda x: f"{x}%"
        )

        df.columns = [
            "Bank",
            "Bank Type",
            "Loan Amount",
            "Interest Rate"
        ]

        st.dataframe(
            df,
            use_container_width=True
        )

        best_loan, lowest_interest = get_recommendations(
            results
        )

        st.subheader("🏆 Recommendations")

        st.success(
            f"Highest Loan Amount: "
            f"{best_loan['bank']} "
            f"(₹{best_loan['loan_amount']:,})"
        )

        st.info(
            f"Lowest Interest Rate: "
            f"{lowest_interest['bank']} "
            f"({lowest_interest['interest_rate']}%)"
        )

        st.metric(
            "Eligible Banks Found",
            len(results)
        )