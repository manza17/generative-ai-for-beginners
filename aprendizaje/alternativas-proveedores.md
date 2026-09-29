# Alternativas gratuitas o de bajo costo para el resto del curso

> Investigación del 2026-09-24, tras terminar los créditos de Azure. Los límites de los free tiers cambian seguido: verifícalos en la consola de cada proveedor antes de usarlos.

## TL;DR — la recomendación

| Rol | Proveedor | Costo | Para qué |
|---|---|---|---|
| **Principal** | **Google Gemini API** (AI Studio) | Gratis, sin tarjeta | Chat, function calling, structured outputs, embeddings. Lecciones 04–08, 11, 15. |
| **Local** | **Ollama** (ya lo tienes instalado, v0.34.2) | Gratis, sin límites | Modelos open source y SLMs (16, 19, 21), embeddings offline, experimentos sin rate limit. |
| **Respaldo rápido** | **Groq** | Gratis, sin tarjeta | Modelos open source (gpt-oss) muy rápidos, si Gemini da 429. |
| **Lección 20** | **Mistral La Plateforme** (modo gratuito) | Gratis, sin tarjeta | Lección 20 con la API nativa de Mistral. |
| **Opcional (carrera)** | **Azure pago por uso** o **Azure for Students** | Céntimos o $100 de crédito | Volver a Foundry más adelante, cuando haga falta para el rol de AI Engineer. |

**La clave:** todos exponen una **API compatible con OpenAI**. El código del curso funciona cambiando 3 cosas: `base_url`, `api_key` y `model`. Lo que aprendiste con `OpenAI(base_url=...)` en la lección 18 es exactamente este patrón.

## Qué necesita cada lección

| Lección | Qué usa | Alternativa |
|---|---|---|
| 01–03, 10, 12–14, 17 | Sin código (teóricas) | Ninguna necesaria |
| 04, 05, 06 | Chat completions | Gemini |
| 07 | Chat + embeddings | Gemini (`gemini-embedding-001`) |
| 08 | Embeddings (búsqueda) | Gemini embeddings u Ollama (`nomic-embed-text`) |
| 09 ✅ | Imágenes | Hecha en Azure |
| 11 | Function calling | Gemini (soporta `tools` en formato OpenAI) |
| 15 | RAG + embeddings | Gemini u Ollama. El curso usaba Azure AI Search, que borramos: revisar al llegar si alcanza con una base vectorial local. |
| 16 | Modelos open source | Ollama |
| 18 ✅ | Fine-tuning | Hecha en Azure |
| 19 | Small Language Models | Ollama (phi, qwen, llama pequeños) |
| 20 | Mistral | Mistral La Plateforme (gratis) |
| 21 | Meta Llama | Ollama (`llama3.2:3b`) o Groq, si sigue ofreciendo Llama |

## Proveedores en detalle

### 1. Google Gemini API: el principal
- **Free tier:** sin tarjeta y sin vencimiento. Aproximadamente 10–15 peticiones/minuto y ~1.500/día, según el modelo. Incluye los modelos **Flash** y **Flash-Lite**. Los modelos **Pro** pasaron a ser de pago en mayo de 2026.
- **Compatible con OpenAI:** `base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"`. Soporta chat, streaming, function calling, embeddings (`gemini-embedding-001`) y structured outputs.
- ⚠️ **Privacidad:** en el free tier, Google **puede usar tus entradas y salidas para entrenar sus modelos**. Para el curso no importa, pero no le envíes datos del trabajo ni datos personales.
- **Cómo obtener la key:** entra en aistudio.google.com y pulsa **Get API key**.

```python
client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
client.chat.completions.create(model="<modelo flash de AI Studio>", messages=[...])
```

### 2. Ollama: local y sin límites
- **Tu equipo:** 16 GB de RAM, **NVIDIA GTX 1650 con 4 GB de VRAM** y 266 GB libres. Ollama ya está instalado.
- **Qué entra en la GPU:** modelos de **~3–4B parámetros** cuantizados (Q4): `llama3.2:3b`, `phi4-mini`, `qwen3:4b`, `gemma3:4b`. Los de 7–8B funcionan, pero parte del modelo pasa a la CPU y van **lentos**.
- **Embeddings:** `nomic-embed-text`. Es liviano y funciona bien en tu equipo.
- **Compatible con OpenAI:** `base_url = "http://localhost:11434/v1"`. La `api_key` puede ser cualquier texto, por ejemplo `"ollama"`.
- **Ventajas:** gratis, offline, sin rate limits y tus datos no salen de tu equipo. Es ideal para las lecciones 16, 19 y 21, que tratan precisamente de modelos abiertos.
- **Desventaja:** la calidad es menor que la de Gemini o GPT, y algunos modelos pequeños hacen function calling de forma poco fiable.

### 3. Groq: respaldo rápido
- **Free tier:** sin tarjeta. Unas 30 peticiones/minuto; los límites diarios y de tokens por minuto dependen del modelo (por ejemplo, `gpt-oss-120b` / `gpt-oss-20b` tienen 1.000/día y 8.000 TPM). Los límites se aplican a toda la organización, no a cada key.
- **Fortaleza:** velocidad muy alta de inferencia.
- **Límite:** no ofrece embeddings, así que no sirve para las lecciones 08 y 15. Hay fuentes que dicen que retiró Llama del free tier: compruébalo en su consola antes de la lección 21.

### 4. Mistral La Plateforme: para la lección 20
- **Modo gratuito:** sin tarjeta, con cuotas **mensuales**. Resérvalo para la lección 20.

### Descartados o secundarios
- **OpenRouter:** unos 14 modelos gratis con una sola key, pero solo ~50 peticiones/día en los gratuitos. Útil para comparar modelos (lección 02), no para trabajar a diario.
- **Cerebras:** desde julio de 2026 es una prueba que pide tarjeta.
- **Cohere:** 1.000 llamadas al mes y solo para uso no comercial.
- **GitHub Models:** retirado.

## Volver a Azure (opcional)
Para tu objetivo de AI Engineer con Azure, conviene tener un camino de vuelta:
- **Azure for Students:** $100 de crédito sin tarjeta, renovable cada año. Requiere ser estudiante **a tiempo completo** de una institución que otorgue títulos, verificado con email académico o carnet. Comprueba si tu diplomatura cumple las condiciones.
- **Pago por uso con alerta de presupuesto:** `gpt-5-nano` cuesta ~$0.05 por millón de tokens de entrada y ~$0.40 de salida. Las lecciones con código gastarían **céntimos**. ⚠️ Las alertas de presupuesto de Azure **avisan pero no cortan** el gasto. El riesgo real está en los recursos con cargo por hora (deployments Standard de fine-tunes, AI Search de pago), no en los tokens.

## Plan para mañana (15 minutos)
1. Crear la key de **Gemini** en AI Studio y guardarla en el `.env` como `GEMINI_API_KEY`.
2. Descargar un modelo en Ollama: `ollama pull llama3.2:3b` y `ollama pull nomic-embed-text`.
3. Adaptar `aprendizaje/leccion-00/python/smoke_test.py` para probar Gemini y Ollama con el mismo código, cambiando solo `base_url`, `api_key` y `model`.
4. Retomar la **lección 01**, que es teórica y no necesita proveedor.
5. (Opcional) Crear la cuenta de Groq como respaldo.

## Fuentes
- [Gemini API — OpenAI compatibility](https://ai.google.dev/gemini-api/docs/openai)
- [Gemini API — Rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Gemini API Free Tier 2026 (pecollective)](https://pecollective.com/tools/gemini-free-tier-guide/)
- [Gemini API Free Tier Limits (TokenMix)](https://tokenmix.ai/blog/gemini-api-free-tier-limits)
- [Groq Free Tier Limits 2026 (TokenMix)](https://tokenmix.ai/blog/groq-free-tier-limits-2026)
- [Groq API Free Tier (Grizzly Peak Software)](https://www.grizzlypeaksoftware.com/articles/p/groq-api-free-tier-limits-in-2026-what-you-actually-get-uwysd6mb)
- [Groq Free Tier 2026 (klymentiev)](https://klymentiev.com/blog/groq-pricing)
- [Free LLM API in 2026: 13 Options Ranked (OpenRouter)](https://openrouter.ai/blog/tutorials/free-llm-apis-compared/)
- [Azure OpenAI Service — Pricing](https://azure.microsoft.com/en-us/pricing/details/azure-openai/)
- [Azure gpt-5-nano pricing (Helicone)](https://www.helicone.ai/llm-cost/provider/azure/model/gpt-5-nano)
- [Azure for Students](https://azure.microsoft.com/en-us/free/students)
- [Azure for Students 2026: Eligibility (Credit for Startups)](https://creditforstartups.com/students/azure-for-students)
