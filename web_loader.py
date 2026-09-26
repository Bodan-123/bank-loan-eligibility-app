import requests
import fitz


def get_pdf_text_from_url(url):

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch PDF. Status Code: {response.status_code}"
        )

    doc = fitz.open(
        stream=response.content,
        filetype="pdf"
    )

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text