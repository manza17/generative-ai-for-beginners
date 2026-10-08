# Lección 04 — Fundamentos de prompt engineering

**Inicio:** 2026-10-05
**Lenguaje(s):** Python

## Objetivos
- Explicar qué es el *prompt engineering* y por qué importa.
- Describir los componentes de un prompt y cómo se usan.
- Aplicar buenas prácticas y técnicas con ejemplos reales (notebook con Gemini y Ollama).

## Conceptos (con mis palabras)
- **Tokenización (Ejercicio 1):** predije ~134 tokens con la regla de ¾ de palabra y salieron 135. `[19]` son 3 tokens (`[`, `19`, `]`): las combinaciones poco frecuentes se parten, y los números se dividen en trozos (por eso a los LLMs les cuestan las cuentas, y los IDs o números largos gastan más tokens de lo que parece). `tiktoken` es el tokenizer de OpenAI: Gemini y Llama tokenizan distinto.
- **Ejercicio 2 — de prompt ambiguo a salida estructurada:**
  1. **Sin instrucción** (`oh say can you see`): Gemini continuó la letra; Ollama reconoció el himno y **alucinó** una letra inventada. Sin instrucción explícita, cada modelo adivina distinto, y un modelo chico (3B) recuerda peor los textos.
  2. **Con instrucción específica** (título ≤ 5 palabras + resumen ≤ 20): los dos hicieron la misma tarea y Ollama no alucinó (ya no tenía que recordar la letra). Pero cada uno usó un formato distinto. Mejor referirse al texto por su **delimitador** que por su posición ("the text above").
  3. **Pidiendo JSON en el prompt** (con `{{ }}` en la f-string): Gemini lo envolvió en ` ```json ` → `json.loads()` falla. Pedir formato en el prompt es **probabilístico**.
  4. **Con `response_format={"type": "json_object"}`**: los dos devolvieron JSON válido. Pero sin el formato en el prompt, Ollama usó el título como clave → JSON válido con **estructura incorrecta** (`KeyError`). `json_object` garantiza JSON, no campos; `json_schema` garantiza campos y tipos; y además se valida en el código.
  5. **Domain understanding matters:** para detectar errores (el himno confundido con el *Pledge of Allegiance*) hay que conocer el dominio; si no, un experto arma el set de prueba y se le da la fuente al modelo (*grounding*).

  📘 **AI-103:** en Azure, Chat Completions usa `response_format={"type": "json_schema", "json_schema": {...}}` y la Responses API usa `text={"format": {"type": "json_schema", ...}}`.
- **Ejercicio 3 — alucinaciones (Guerra Marciana de 2076):**
  1. **Sin salida**: los dos inventaron un plan de clase completo y profesional, mezclando **hechos reales** (Outer Space Treaty de 1967, Olympus Mons, Phobos) con **ficción** (un gobernador, un libro y unos tratados inexistentes). Esa mezcla es lo que hace peligrosas las alucinaciones. El modelo siguió la premisa (como el Titanic de la lección 03).
  2. **Con "do not make it up" dentro de los delimitadores**: Ollama inventó todavía más (URL, autor y una fecha imposible: 30/02). Las instrucciones van **fuera** de los delimitadores, que marcan datos.
  3. **Con la instrucción fuera y una salida (*give the model an out*)**: los dos se negaron a inventar, y Ollama ofreció una alternativa.
  4. **Premisa falsa plausible** ("plan de clase sobre el Tratado de Córdoba de 1823 entre Argentina y Chile"): Gemini detectó que no existe y ofreció alternativas reales (Tratados de Córdoba de México 1821, Tratado de Límites de 1881); **Ollama inventó el contenido**. Diferencia clara entre un modelo grande y uno de 3B. ⚠️ Aun así, entre las alternativas de Gemini aparece un "Tratado de Pancien (1823)" que no está verificado: incluso cuando se niega a inventar, **hay que validar lo que sugiere**.
  5. **Trampa de los notebooks**: editar una celda no cambia nada hasta ejecutarla; el kernel usa lo que tiene en memoria. Ante la duda: Restart y ejecutar en orden.
  6. **Matices**: el *out* reduce pero no elimina las alucinaciones, sobre todo con premisas falsas **plausibles**. Además, si el modelo responde "no sé" en texto libre, el backend no puede detectarlo. Se resuelve pidiendo un JSON con un campo que lo indique:
     ```python
     prompt = f"""Create a lesson plan about the topic delimited by triple backticks.
     If the topic is not a real event or you don't know it, set "known" to false and "lesson_plan" to null.
     Respond only with JSON in this format: {{"known": true, "lesson_plan": "..."}}
     ```{text}```"""

     datos = json.loads(get_completion(prompt, as_json=True))
     if not datos["known"]:
         mostrar("No tenemos información confiable sobre ese tema.")   # el backend decide, no el modelo
     else:
         mostrar(datos["lesson_plan"])
     ```
     (Con `json_schema` + `"required": ["known", "lesson_plan"]` se garantiza que el campo `known` siempre exista.)
- **Ejercicio 4 — prompt por instrucciones (resumen de Júpiter para segundo grado):**
  1. **Solo "para un alumno de segundo grado"**: los dos simplificaron el vocabulario y eliminaron "una milésima parte de la masa del Sol". Sin formato ni largo, no coincidieron (Ollama: 3 párrafos y *"Hey kiddo!"*; Gemini: 1 párrafo neutro). Ollama **inventó** que la gente creía que Júpiter era "el ojo de un dios": falla de ***groundedness*** (lección 03). Ambigüedad: ¿el texto es **para leérselo** al niño o **para el docente**?
  2. **Prompt mejorado**:
     ````
     Summarize content you are provided with for a second-grade student. Keep the result to one paragraph with 3-5 bullet points.
     The summary should be concise and brief. Keep in mind that it is intended for a teacher to use with children around nine years old. Do not invent content; use only the information found in the text.
     ```{text}```
     ````
     Los dos usaron viñetas, entendieron que era para el docente y desapareció "el ojo de un dios". Ollama agregó una analogía ("como ponerle nombre a una mascota"): inventó menos, pero no cero. "Second grade" frente a "nine years old" fue una prueba piloto: el modelo sigue la instrucción más específica. En un prompt real, evitar contradicciones.
  3. **Cue** (*"Jupiter is the largest planet..."* después de los datos): no eliminó la frase introductoria en ninguno. Un *cue* debe ir **al final de todo** y ser el **inicio literal de la salida** (*"Fun facts about Jupiter:\n•"*). Con modelos de chat funciona peor que con la antigua Completion API. Solución: instrucción explícita (*"Start directly with the first bullet"*) o, de forma determinista, un JSON `{"facts": [...]}`.
  4. **Error conceptual de Ollama**: al simplificar dijo que Júpiter "bloquea la luz del Sol" para hacer sombras; es al revés (su luz reflejada ilumina los objetos). Simplificar es reformular, y un modelo chico puede **distorsionar** el hecho: la *groundedness* se evalúa, no basta con pedirla.
- **Ejercicio 5 — prompt complejo (mensajes system/user/assistant):**
  1. Chat Completions recibe una **lista de mensajes**: `system` (personalidad y reglas, el metaprompt), `user` (pregunta) y `assistant` (respuestas anteriores). El mensaje `assistant` **lo puedo escribir yo**, y el modelo lo toma como algo que dijo: por eso mantuvo el tono sarcástico (es un tipo de *few-shot*).
  2. *"Where was it played?"* con historial: los dos respondieron **Globe Life Field, Arlington** (sede neutral por la pandemia), con sarcasmo. Mi predicción de que "no se jugó" era falsa. Dato muy frecuente en los datos de entrenamiento → hasta el modelo de 3B lo sabe.
  3. **Sin el historial**: los dos pidieron contexto. **La API no tiene memoria** (*stateless*): el contexto existe solo si lo envío.
  4. 📘 **AI-103:** Chat Completions = el historial lo guarda mi backend y lo reenvío completo. Responses API = el servidor lo guarda y encadeno con `previous_response_id` (solo el mensaje nuevo). No funciona con `store=False`, y el contexto anterior **se sigue cobrando** como entrada.
- **Challenge — cue del Volvo** (*"Complete the sentence: Show me an image of red car of make Volvo and "*): Gemini dio opciones con explicaciones alrededor; Ollama continuó la frase sin más (se comportó más como un modelo de completado). **Prompt mejorado**: *"You must respond with a single sentence, incorporating details such as the year, the location, and the number of people inside the car. The goal is for the finished sentence to serve as a clear and precise prompt for generating an image using a model like gpt-image-2.5-flare."* Los dos generaron prompts de imagen detallados (darle el **objetivo** ayuda a elegir detalles visuales), pero **Ollama perdió el color rojo**: al reescribir, un modelo puede descartar requisitos del original → pedir explícitamente que los conserve y validarlo. Usar un LLM para generar el prompt de otro modelo es ***prompt chaining*** (lección 05).
- **Knowledge check** (¿cuál es el mejor prompt de imagen?): orden **2 > 3 > 1**. La 2 describe el auto (marca, modelo, color), el lugar (acantilado) y el momento (*sun setting* = atardecer, no solo "de día": define la luz de la imagen). La 3 describe el auto pero no la escena. La 1 deja casi todo librado al modelo: lo que no especifico, lo decide él, y probablemente no sea lo que esperaba. Buena práctica: **"Be specific and clear"**.
- **Explore Your Intuition — system prompt de Bartun (borrador):** aplicó rol y tono, datos del negocio en el system y *few-shot* con un mensaje `assistant` (con transparencia: "I'm Bartun, the AI assistant"). Hallazgos:
  1. 🔴 **Alucinación de acción**: los dos dijeron "I've got you booked" sin poder reservar. La IA no confirma: devuelve una **intención en JSON** (`{"accion": "reservar", ...}`) y el **backend** reserva y confirma (lección 11, *function calling*).
  2. 🟠 **El modelo no sabe la fecha de hoy**: "tomorrow" no significa nada para él. Hay que **inyectar la fecha** en el system prompt con la f-string (`{date.today()}`).
  3. 🟠 **Ollama distorsionó la política** (inventó "30 días" y otras reglas). Política entre delimitadores y citada textualmente, o enviada por el backend como texto fijo.
  4. 🟡 **Gemini reservó antes de saber el servicio**: definir qué datos son obligatorios y pedirlos **antes** de reservar.
  - **¿Puede el asistente decir "reservado" si el backend lo confirma?** Sí: el flujo es modelo → intención (JSON) → **backend reserva** → el resultado real (OK o error, con fecha y hora) se le devuelve al modelo como un mensaje más → el modelo redacta la confirmación **basándose en ese resultado**. Así nunca confirma algo que no pasó. Para datos críticos (fecha y hora exactas), lo más seguro es que el backend arme la confirmación con un texto fijo, o validar que el modelo no los cambió.
- **Parámetro opcional en Python**: armar un dict con los argumentos y desempaquetarlo con `**params` (equivale al spread condicional de TS: `...(cond && {...})`).

## Qué hice
<!-- ✏️ Completado por Claude a partir de la sesión; cámbialo con tus palabras si quieres. -->
- Configuré Gemini (free tier) y Ollama (`llama3.2:3b`) y adapté el notebook del curso de la Responses API de Azure a Chat Completions, con un `PROVIDER` para cambiar de modelo.
- Hice los 5 ejercicios comparando Gemini y Ollama con el mismo prompt, iterando cada prompt según los resultados.
- Agregué al notebook celdas "📘 Referencia AI-103" con la versión Azure (clientes, Responses vs Chat Completions, structured outputs, `previous_response_id`).
- Escribí un borrador del system prompt de Bartun aplicando las técnicas de la lección.

## Código y ejercicios
- `python/aoai-assignment.ipynb` — copia adaptada a Gemini/Ollama (Chat Completions), con `get_completion(prompt, as_json=False)` y referencias Azure para el AI-103.
- `ai-103.md` — resumen de lo de Azure de esta lección para la certificación.

## Dudas pendientes
- [ ] 

## Resumen en una frase
Un buen prompt deja poco librado al modelo —instrucción específica, datos delimitados, roles, ejemplos y una salida para cuando no sabe— y lo que debe ser exacto (formato, fecha, acciones) lo garantiza el código, no el modelo.

### Resumen extendido (con mis palabras, corregido ✏️)
Aunque esta lección incluyó bastante configuración, describo lo aprendido. Vimos la importancia del *prompt engineering* y los resultados que provocan los prompts "vagos": si dejas que el modelo decida lo que quieres hacer, rara vez llegarás a lo que realmente esperabas. Por eso es importante conocer los componentes del prompt y cómo se usan.

Una lista de mensajes con roles es esencial para un asistente como el que tengo pensado hacer: `system` define la personalidad y las reglas del asistente, `user` es lo que escribe el usuario y `assistant` lo que respondió el modelo. Este flujo da resultados más acordes a lo esperado porque plantea la situación real.
> ✏️ Dos matices: los mensajes `assistant` **también los puedo escribir yo**, como ejemplos (*few-shot*), y el modelo los toma como propios. Y la API **no tiene memoria**: el "flujo" existe solo porque le reenvío el historial en cada llamada.

Por último, hicimos un ejercicio que engloba todo lo aprendido, y comprendí que el modelo no sabe la fecha de hoy: se la tengo que inyectar.
> ✏️ Antes decía "el modelo no puede manejar fechas". Sí puede razonar con fechas si se las doy; lo que **no sabe** es qué día es hoy, porque no tiene reloj. Por eso se inyecta `{date.today()}` en el system prompt.

> ✏️ Agregados dos aprendizajes centrales que no estaban: (1) pedir un formato en el prompt es **probabilístico**: `json_object` garantiza JSON válido y `json_schema` garantiza los campos; (2) los modelos **alucinan** también **acciones** ("I've got you booked"): la IA devuelve una intención y el backend ejecuta y confirma.
