from pypdf import PdfReader
import os
import pickle
from openai import OpenAI

client = OpenAI()

textos = []

for archivo in os.listdir("pdfs"):
    if archivo.endswith(".pdf"):
        reader = PdfReader(f"pdfs/{archivo}")
        for page in reader.pages:
            texto = page.extract_text()
            if texto:
                textos.append(texto[:1000])

embeddings = []

for t in textos:
    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=t
    )
    embeddings.append(emb.data[0].embedding)

with open("base.pkl", "wb") as f:
    pickle.dump((textos, embeddings), f)

print("✅ Base creada")