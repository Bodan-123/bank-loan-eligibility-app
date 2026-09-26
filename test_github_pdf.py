import requests
import fitz

url = "https://raw.githubusercontent.com/Bodan-123/bank-loan-eligibility/main/standard_report.pdf"

response = requests.get(url)

print("Status Code:", response.status_code)

doc = fitz.open(
    stream=response.content,
    filetype="pdf"
)

for page in doc:
    print(page.get_text())

doc.close()