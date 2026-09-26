from langchain_text_splitters import RecursiveCharacterTextSplitter
import json


def create_chunks(text):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_text(text)

    return chunks


if __name__ == "__main__":

    with open(
        "documents/extracted_text.txt",
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    chunks = create_chunks(text)

    print(f"Total Chunks Created: {len(chunks)}")

    with open(
        "documents/chunks.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(chunks, file, indent=4)

    print("Chunks saved successfully.")