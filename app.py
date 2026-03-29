from fastapi import FastAPI
from openai import OpenAI
import os
import pickle
import numpy as np

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# cargar base
with open("base.pkl", "rb") as f:
    textos, embeddings = pickle.load(f)

def similitud(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

@app.get("/")
def inicio():
    return {"mensaje": "API jurídica funcionando 🚀"}

@app.get("/pregunta")
def preguntar(q: str):

    emb_query = client.embeddings.create(
        model="text-embedding-3-small",
        input=q
    ).data[0].embedding

    resultados = []
    for i in range(len(textos)):
        score = similitud(emb_query, embeddings[i])
        resultados.append((score, textos[i]))

    mejores = sorted(resultados, reverse=True)[:3]

    contexto = "\n\n".join([m[1] for m in mejores])

    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Responde como experto en derecho chileno usando el contexto entregado."},
            {"role": "user", "content": f"Contexto:\n{contexto}\n\nPregunta:\n{q}"}
        ]
    )

    return {
        "respuesta": respuesta.choices[0].message.content
    }
