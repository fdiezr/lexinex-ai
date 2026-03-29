from fastapi import FastAPI
from openai import OpenAI
import os
import pickle
import numpy as np

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Cargar base
with open("base_conocimiento.pkl", "rb") as f:
    base = pickle.load(f)

def similitud(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

@app.get("/")
def read_root():
    return {"mensaje": "API jurídica funcionando 🚀"}

@app.get("/pregunta")
def preguntar(q: str):
    
    # embedding de la pregunta
    emb_query = client.embeddings.create(
        model="text-embedding-3-small",
        input=q
    ).data[0].embedding

    # buscar los textos más cercanos
    mejores = sorted(
        base,
        key=lambda x: similitud(emb_query, x["embedding"]),
        reverse=True
    )[:3]

    contexto = "\n\n".join([m["texto"] for m in mejores])

    # generar respuesta
    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Responde como experto en derecho chileno usando el contexto entregado."},
            {"role": "user", "content": f"Contexto:\n{contexto}\n\nPregunta:\n{q}"}
        ]
    )

    return {
        "respuesta": respuesta.choices[0].message.content,
        "contexto_usado": contexto[:500]
    }