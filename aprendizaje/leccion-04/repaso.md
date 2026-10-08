# Repaso — Lección 04: Fundamentos de prompt engineering

> Sesiones del 5 al 8 de octubre de 2026.
> Código: [`python/aoai-assignment.ipynb`](python/aoai-assignment.ipynb) · Notas: [`notas.md`](notas.md) · Azure: [`ai-103.md`](ai-103.md)

## 1. Qué hicimos, en orden
1. **Setup de proveedores:** key de Gemini en AI Studio, `llama3.2:3b` en Ollama y una prueba de humo con los dos ([`smoke_test_providers.py`](../leccion-00/python/smoke_test_providers.py)).
   - `gemini-2.5-flash` → `404`: ya no está disponible para cuentas nuevas.
   - `gemini-3.8-flash` → `503`: estaba saturado.
   - Solución: `gemini-3.5-flash-lite` + `max_retries=5`.
2. **Adaptación del notebook:** de la Responses API de Azure a **Chat Completions**, con un `PROVIDER` para alternar entre Gemini y Ollama, y celdas "📘 Referencia AI-103" con la versión de Azure.
3. **Ejercicios 1–5, más el challenge y "Explore Your Intuition"**, comparando siempre los dos modelos con el mismo prompt.

## 2. El código

### Cliente con dos proveedores (Ejercicio 2)
```python
PROVIDER = "gemini"   # o "ollama"
PROVEEDORES = {
    "gemini": {"base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
               "api_key": os.environ.get("GEMINI_API_KEY"), "model": os.environ.get("GEMINI_MODEL")},
    "ollama": {"base_url": "http://localhost:11434/v1", "api_key": "ollama",
               "model": os.environ.get("OLLAMA_MODEL", "llama3.2:3b")},
}
cfg = PROVEEDORES[PROVIDER]
client = OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"], max_retries=5)
```
- Los dos son **compatibles con la API de OpenAI**: solo cambian `base_url`, `api_key` y `model`.
- Ollama no valida la key, pero el cliente exige una.
- `max_retries` reintenta con espera creciente ante errores `429` y `503`.

### `get_completion` con parámetro opcional
```python
def get_completion(prompt, as_json=False):
    params = {"model": deployment,
              "messages": [{"role": "user", "content": prompt}],
              "max_tokens": 1024}
    if as_json:
        params["response_format"] = {"type": "json_object"}
    response = client.chat.completions.create(**params)
    return response.choices[0].message.content
```
- No se puede poner un `if` dentro de los argumentos: se arma un **dict** y se desempaqueta con `**params`.
- Es el equivalente del *spread* condicional de TS: `...(asJson && { response_format })`.

### Prompt con instrucción, delimitadores y salida
```python
prompt = f"""Create a lesson plan about the topic delimited by triple backticks.
If the topic is not a real event or you don't know it, set "known" to false and "lesson_plan" to null.
Respond only with JSON in this format: {{"known": true, "lesson_plan": "..."}}
```{text}```"""
```
- La **instrucción va fuera** de los delimitadores; los delimitadores marcan **datos**.
- `{{ }}` son **llaves literales** en una f-string. Con llaves simples, Python intenta evaluar el contenido.
- La salida (*out*) le da al modelo permiso para decir "no sé", y `known` le permite al **backend** detectarlo.

### Mensajes system / user / assistant (Ejercicio 5)
```python
messages=[
    {"role": "system", "content": "You are a sarcastic assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "Who do you think won? The Los Angeles Dodgers of course."},
    {"role": "user", "content": "Where was it played?"},
]
```
- El mensaje `assistant` **lo escribo yo**, y el modelo lo toma como propio. Es un tipo de *few-shot*: por eso mantuvo el sarcasmo.
- **La API no tiene memoria:** sin los 3 primeros mensajes, los dos modelos pidieron contexto.

## 3. Lo que mostró cada ejercicio
| Ejercicio | Hallazgo |
|---|---|
| 1. Tokenización | Predije ~134 tokens y salieron 135. `[19]` son 3 tokens: los números y las combinaciones raras se parten. |
| 2. Sin instrucción | Gemini continuó el himno; Ollama alucinó una letra. Sin instrucción, cada modelo adivina distinto. |
| 2. JSON | Pedido en el prompt: Gemini lo envolvió en ` ```json `. `json_object`: JSON válido, pero Ollama usó el título como clave. → `json_schema` + validación. |
| 3. Alucinaciones | Los dos inventaron la Guerra Marciana mezclando hechos reales con ficción. Con la instrucción fuera de los delimitadores y una salida, los dos se negaron. Ante una premisa falsa **plausible** (el Tratado de Córdoba de 1823), Gemini detectó el error y Ollama inventó. |
| 4. Instrucciones | El público cambia el resultado. Ollama inventó "el ojo de un dios" (*groundedness*) y luego distorsionó cómo se forman las sombras. El *cue* no eliminó la introducción. |
| 5. Mensajes | Los dos acertaron Globe Life Field: es un dato frecuente. Sin historial, pidieron contexto. |
| Challenge | Ollama continuó la frase como un modelo de completado. Al reescribir, perdió el color rojo. |
| Bartun | **Alucinación de acción** ("I've got you booked"), el modelo no sabe la fecha de hoy, Ollama distorsionó la política y Gemini reservó antes de saber el servicio. |

**La constante de toda la lección:** el modelo chico (3B) sigue peor las instrucciones, alucina más y **distorsiona al reformular**.

## 4. Las buenas prácticas, con mis ejemplos
| Práctica | Mi ejemplo |
|---|---|
| Ser específico y claro | Título ≤ 5 palabras + resumen ≤ 20 → los dos hicieron la misma tarea |
| Separar instrucciones y contenido | La instrucción dentro de ` ``` ` → Ollama inventó más |
| Few-shot | El mensaje `assistant` sarcástico; el ejemplo de diálogo de Bartun |
| *Cues* | El Volvo: Ollama continuó la frase; Gemini dio opciones |
| Darle una salida al modelo | "Si no sabes, `known: false`" → los dos se negaron a inventar |
| Conocer el dominio | No detecté el *Pledge of Allegiance*; sí habría detectado un error sobre Argentina |
| Evitar contradicciones | "Segundo grado" frente a "nueve años": el modelo sigue la instrucción más específica |

## 5. Gotchas
| Problema | Causa | Solución |
|---|---|---|
| `404` en Gemini | Modelo retirado para cuentas nuevas | Listar los modelos disponibles; no hardcodear nombres |
| `503` en Gemini | Modelo saturado (free tier, baja prioridad) | `max_retries`; usar Flash-Lite |
| `json.loads` falla | El JSON viene envuelto en ` ```json ` | `response_format` en la API |
| `KeyError` con JSON válido | `json_object` no garantiza campos | `json_schema` + validar en el código |
| Sigue saliendo JSON tras editar la función | El kernel usaba la versión vieja en memoria | Ejecutar la celda de nuevo, o Restart + ejecutar en orden |
| Error con `{` en una f-string | Llaves interpretadas como variables | Escribir llaves dobles `{{ }}` |
| "Mañana" sin sentido | El modelo no sabe la fecha de hoy | Inyectar `{date.today()}` en el system prompt |
| "I've got you booked" sin reservar | El modelo afirma acciones que no ejecutó | Intención en JSON → el backend reserva → el modelo confirma con el resultado real |

## 6. Preguntas de autoevaluación
1. ¿Por qué `{"type": "json_object"}` no alcanza para un backend? ¿Qué agrega `json_schema`?
2. Le pides a un modelo de chat *"Where was it played?"* y responde bien. En la llamada siguiente, con la misma pregunta, pide contexto. ¿Qué cambió en tu código?
3. ¿Dónde va la instrucción respecto de los delimitadores, y por qué?
4. ¿Por qué un modelo pequeño es más riesgoso cuando le pides **simplificar** o **reescribir** un texto?
5. Bartun le dice a un cliente "tu turno quedó reservado", pero en el calendario no aparece. ¿Qué falló en el diseño y cómo se corrige?
