import fitz
import re


def extract_text(pdf_path):

    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()

    doc.close()

    return text


def extract_user_details(text):

    user_data = {}

    name = re.search(
        r"Applicant Name\s*:\s*([A-Za-z ]+)",
        text,
        re.MULTILINE
    )

    aadhaar = re.search(
        r"Aadhaar Number\s*:\s*(\d{12})",
        text,
        re.MULTILINE
    )

    pan = re.search(
        r"PAN Number\s*:\s*([A-Z]{5}[0-9]{4}[A-Z])",
        text,
        re.MULTILINE
    )

    company = re.search(
        r"Company Name\s*:\s*([A-Za-z ]+)",
        text,
        re.MULTILINE
    )

    salary = re.search(
        r"Salary Per Annum\s*:\s*INR\s*([\d,]+)",
        text,
        re.MULTILINE
    )

    user_data["name"] = name.group(1).strip() if name else None
    user_data["aadhaar"] = aadhaar.group(1).strip() if aadhaar else None
    user_data["pan"] = pan.group(1).strip() if pan else None
    user_data["company"] = company.group(1).strip() if company else None

    if salary:
        salary_value = salary.group(1).replace(",", "")
        user_data["salary"] = int(salary_value)
    else:
        user_data["salary"] = None

    return user_data


if __name__ == "__main__":

    pdf_path = "documents/user_reports/user_report_1.pdf"

    text = extract_text(pdf_path)

    user_data = extract_user_details(text)

    print("\nExtracted User Data:\n")
    print(user_data)