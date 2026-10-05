"""Prueba de humo: Gemini (nube, free tier) y Ollama (local) con el mismo cliente OpenAI.

Solo cambian base_url, api_key y model: el resto del código es idéntico.
"""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVEEDORES = {
    "Gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "api_key": os.getenv("GEMINI_API_KEY"),
        "model": os.getenv("GEMINI_MODEL"),
    },
    "Ollama": {
        "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
        "api_key": "ollama",  # Ollama no valida la key, pero el cliente exige una
        "model": os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
    },
}

for nombre, cfg in PROVEEDORES.items():
    print(f"\n=== {nombre} ===")
    if not cfg["api_key"]:
        print("Falta la key en el .env: se omite.")
        continue

    # max_retries: reintenta con espera creciente ante 429/503 (saturación temporal del free tier)
    client = OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"], max_retries=5)

    if not cfg["model"]:
        # Sin modelo configurado: lista los disponibles para elegir uno
        print("Falta el modelo en el .env. Modelos disponibles:")
        for m in client.models.list():
            print(" -", m.id)
        continue

    try:
        response = client.chat.completions.create(
            model=cfg["model"],
            messages=[{"role": "user", "content": "Responde solo: OK"}],
        )
        print("Modelo:", cfg["model"])
        print("Respuesta:", response.choices[0].message.content)
    except Exception as err:  # en una prueba de humo queremos ver cualquier error, sin traceback largo
        print(f"Error ({type(err).__name__}): {err}")
