from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Lexinex AI</title>
        </head>
        <body style="font-family: Arial; max-width: 700px; margin: auto; padding-top: 40px;">
            
            <h2>Lexinex AI ⚖️</h2>

            <p>Asistente jurídico con inteligencia artificial.</p>

            <button onclick="suscribirse()" style="padding:10px; background:black; color:white;">
                Suscribirme (acceso ilimitado mensual)
            </button>

            <br><br>

            <input id="pregunta" style="width:100%; padding:10px;" placeholder="Escribe tu pregunta jurídica..." />
            
            <button onclick="enviar()" style="margin-top:10px; padding:10px;">
                Preguntar
            </button>

            <pre id="respuesta" style="margin-top:20px; white-space: pre-wrap;"></pre>

            <script>
                async function enviar() {
                    const q = document.getElementById("pregunta").value;
                    const res = await fetch(`/pregunta?q=${encodeURIComponent(q)}`);
                    const data = await res.json();
                    document.getElementById("respuesta").innerText = data.respuesta || data.error;
                }

                function suscribirse() {
                    window.location.href = "https://link.mercadopago.cl/lexinex";
                }
            </script>

        </body>
    </html>
    """

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

        texto = respuesta.choices[0].message.content

        texto_final = texto + "\\n\\n---\\nSi tienes dudas adicionales, puedes escribir a fdiezr@udd.cl"

        return {"respuesta": texto_final}

    except Exception as e:
        return {"error": str(e)}
