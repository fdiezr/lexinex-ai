from fastapi import FastAPI
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def inicio():
    return {"mensaje": "API jurídica funcionando 🚀"}

@app.get("/pregunta")
def preguntar(q: str):
    try:
        respuesta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un abogado experto en derecho chileno."},
                {"role": "user", "content": q}
            ]
        )

        return {
            "respuesta": respuesta.choices[0].message.content
        }

    except Exception as e:
        return {
            "error": str(e)
        }
