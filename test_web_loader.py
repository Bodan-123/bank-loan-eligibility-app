from web_loader import get_pdf_text_from_url

url = "https://raw.githubusercontent.com/Bodan-123/bank-loan-eligibility/main/standard_report.pdf"

text = get_pdf_text_from_url(url)

print(text[:2000])