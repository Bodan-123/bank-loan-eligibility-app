# Bank Loan Eligibility Analyzer

A Python and Streamlit demo that reads an applicant's loan report PDF, extracts
the applicant details, and compares the annual salary against bank eligibility
rules stored in a local SQLite database. It displays matching offers and
highlights the highest loan amount and lowest interest rate.

## Requirements

- Python 3.10 or newer
- Internet access for installing the dependencies and downloading the sample
  bank rules

## Setup

From the project directory, create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Initialize the local bank rules database from the public sample report:

```powershell
python -m extraction.rule_extractor
```

This downloads the sample `standard_report.pdf` from the
[bank-loan-eligibility repository](https://github.com/Bodan-123/bank-loan-eligibility)
and saves the extracted rules to `bank_rules.db` in the project directory.

## Run the app

```powershell
python -m streamlit run app.py
```

Open the local URL printed by Streamlit, upload an applicant report PDF, and
review the extracted details and matching sample offers.

## Privacy and generated files

The app displays the applicant details extracted from the uploaded PDF. Use
synthetic or appropriately authorized documents when trying the demo, and take
care not to expose sensitive personal information.

Local inputs and generated data—including `documents/`, `bank_rules.db`, the
Chroma vector store, and the Python virtual environment—are excluded from Git.
They need to be created or provided locally as required; the sample applicant
PDFs and generated databases are not included in this repository.

## Project structure

- `app.py` — Streamlit user interface.
- `ingestion/` — PDF parsing, text chunking, embeddings, and vector-store
  helpers.
- `extraction/rule_extractor.py` — Loads sample eligibility rules into SQLite.
- `eligibility/eligibility_engine.py` — Matches annual salary to stored rules
  and selects offer recommendations.
- `database/`, `retrieval/`, `reports/`, and `utils/` — Supporting modules.

This is a demonstration project, not a lending decision or financial advice.
