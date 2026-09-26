import json
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

with open(
    "documents/chunks.json",
    "r",
    encoding="utf-8"
) as file:
    chunks = json.load(file)

embeddings = model.encode(chunks)

np.save(
    "documents/embeddings.npy",
    embeddings
)

print("Embeddings saved successfully")