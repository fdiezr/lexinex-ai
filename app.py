from fastapi import FastAPI
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key="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")

# 📁 Ruta fija a tu carpeta
CARPETA_PDFS = "/Users/felipediez/Desktop/LEXINEX"

def leer_pdfs():
    texto = ""

    try:
        from pypdf import PdfReader

        for archivo in os.listdir(CARPETA_PDFS):
            if archivo.endswith(".pdf"):
                ruta = os.path.join(CARPETA_PDFS, archivo)
                reader = PdfReader(ruta)

                for pagina in reader.pages:
                    contenido = pagina.extract_text()
                    if contenido:
                        texto += contenido + "\n"

    except Exception as e:
        print("ERROR leyendo PDFs:", str(e))
        return f"Error leyendo PDFs: {str(e)}"

    if not texto.strip():
        return "No se pudo extraer texto de los PDFs."

    return texto


@app.get("/")
def read_root():
    return {"mensaje": "API funcionando 🚀"}


@app.get("/pregunta")
def preguntar(q: str):
    contexto = leer_pdfs()

    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
Eres un asistente legal experto de LEXINEX.

Debes responder principalmente usando la información contenida en los PDFs.

Si no encuentras la respuesta en los documentos, puedes complementar con conocimiento jurídico general.

CONTEXTO:
{contexto}
"""
            },
            {"role": "user", "content": q}
        ]
    )

    return {"respuesta": respuesta.choices[0].message.content}