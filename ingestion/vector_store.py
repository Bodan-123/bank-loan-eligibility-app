import json
import chromadb
from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# Load chunks
with open(
    "documents/chunks.json",
    "r",
    encoding="utf-8"
) as file:

    chunks = json.load(file)


# Create ChromaDB Client
client = chromadb.PersistentClient(
    path="chroma_db"
)

# Create Collection
collection = client.get_or_create_collection(
    name="bank_rules"
)

# Store chunks
for i, chunk in enumerate(chunks):

    embedding = model.encode(chunk).tolist()

    collection.add(
        ids=[str(i)],
        documents=[chunk],
        embeddings=[embedding]
    )

print("Data stored in ChromaDB successfully.")