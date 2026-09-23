"""Prueba de humo: verifica que el .env y el deployment de Azure OpenAI funcionan."""
import os

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
)

response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],  # nombre del deployment, no del modelo
    messages=[{"role": "user", "content": "Responde solo: OK"}],
)

print("Deployment:", os.environ["AZURE_OPENAI_DEPLOYMENT"])
print("Respuesta:", response.choices[0].message.content)
