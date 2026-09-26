import fitz


def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF using PyMuPDF.
    """

    text = ""

    pdf_document = fitz.open(pdf_path)

    for page in pdf_document:
        text += page.get_text()

    pdf_document.close()

    return text


if __name__ == "__main__":

    pdf_path = "documents/standard_report.pdf"

    extracted_text = extract_text_from_pdf(pdf_path)

    with open(
        "documents/extracted_text.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(extracted_text)

    print("Text extraction completed successfully.")