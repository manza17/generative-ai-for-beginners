# Lección 01 — Introducción a la IA generativa y los LLMs

**Inicio:** 2026-09-23
**Lenguaje(s):** — (lección teórica, sin código)

## Objetivos
- Entender qué es la IA generativa y cómo encaja en IA ⊃ ML ⊃ DL ⊃ GenAI.
- Entender cómo funciona un LLM por dentro: tokens, predicción del siguiente token y sampling.
- Conocer para qué sirve un LLM y sus límites (alucinaciones, no-determinismo).

## Conceptos (con mis palabras)
- **IA:** cualquier sistema que imita una capacidad humana. Al principio se programaba con reglas escritas a mano.
- **Machine Learning (ML):** el sistema aprende patrones de los datos en lugar de seguir reglas.
- **Deep Learning (DL):** ML con redes neuronales de muchas capas.
- **IA Generativa (GenAI):** DL que crea contenido nuevo (texto, imágenes) en lugar de solo clasificar.
- **Idea general de IA → ML → DL → GenAI:** cada capa sustituye reglas escritas a mano por patrones aprendidos de los datos, y la IA generativa añade la capacidad de crear, no solo de clasificar.
- **IA ⊃ ML ⊃ DL ⊃ GenAI:** clasificar no es generar. Es GenAI solo si crea contenido nuevo (no una plantilla fija). Para clasificar tickets alcanza con ML clásico.
  > ✏️ Movidas desde "Resumen en una frase": esa sección es para una única frase propia al cerrar la lección.
- **Transformer y atención:** a diferencia de la RNN (secuencial, como un `for` con `await`), procesa todas las palabras en paralelo (como `Promise.all`) y por eso aprovecha la GPU. El costo: la memoria crece de forma cuadrática (n²) con el largo del texto (doble de texto → 4× memoria).
- **Resumen del bloque 1:** la IA generativa es Deep Learning que crea contenido, y el Transformer la hizo viable porque procesa en paralelo, a cambio de más memoria.
- **Tokens:** el modelo no ve palabras, ve IDs de tokens. El token es la unidad de costo y de contexto. En español se gastan más tokens que en inglés. Los espacios también cuentan: minificar el JSON o enviar solo los campos necesarios abarata la llamada.
- **Predicción del siguiente token:** el LLM genera de a un token en bucle (autoregresivo). La entrada se procesa en una pasada en paralelo (*prefill*) [como lo haría un `Promise.all`: todos los tokens del prompt a la vez]; la salida necesita una pasada por token (*decode*) [como un `while` con `await`: cada vuelta espera a la anterior y produce un solo token]. Por eso los tokens de salida son más caros y lentos, y conviene limitar la longitud de la respuesta.
- **Cuello de botella, TTFT y tokens/s:** el cuello de botella es la parte más lenta, la que limita el total. Un documento largo con respuesta corta se nota en el TTFT (prefill: paralelo pero con mucho trabajo, pantalla en blanco). Un prompt corto con respuesta larga se nota en el tiempo de decode; se mitiga con streaming. El largo del bucle depende de la respuesta, no del documento.
- **Probabilidades y temperatura:** el modelo calcula una distribución de probabilidad sobre todo su vocabulario y luego sortea (*sampling*); por eso no es determinista. Temperatura baja: predecible (para extraer datos). Alta: creativa pero con más errores. Temperatura baja reduce la variabilidad, **no los errores**: la precisión se asegura validando (esquemas, código, revisión humana). Los modelos de razonamiento (`gpt-5-mini`) solo aceptan temperature = 1.
- **El ciclo completo de un LLM (B → D → A → C, y vuelve a D):**
  ```ts
  let tokens = tokenizar(prompt);            // B: tokenizar el prompt (una sola vez → prefill)
  while (true) {
    const probs = modelo.predecir(tokens);   // D: calcular probabilidades del siguiente token
    const siguiente = sortear(probs, temp);  // A: sortear el token según la temperatura
    tokens.push(siguiente);                  // C: agregar el token a la entrada
  }                                          // D → A → C se repite por cada token → decode
  ```
- **Prompt y completion:** el prompt es lo que envío y la completion lo que genera el modelo (completa texto token a token). Tipos de prompt: instrucción, pregunta, texto a completar y código, y se pueden combinar. Conviene distinguir la **instrucción** (qué hacer) de los **datos** (sobre qué hacerlo).
- **Alucinaciones:** respuestas falsas con total seguridad. El modelo optimiza lo **plausible**, no lo **verdadero**. Alucina más con datos poco frecuentes en su entrenamiento (distribución plana → el sorteo elige algo inventado) y con datos posteriores a su **knowledge cutoff**. Se mitiga dándole los datos en el prompt (RAG, herramientas) y validando.
- **Resumen del bloque 2:** un LLM convierte el texto en tokens, predice el siguiente token con probabilidades, lo sortea según la temperatura y repite en bucle hasta terminar.
- **Resumen del bloque 3:** todo lo que hace un LLM es completar texto; el tipo de prompt y los datos que le das definen la tarea.
- **Resumen del bloque 4:** un LLM no es inteligente, ni determinista, ni fiable por sí solo: es un primer borrador muy rápido que hay que validar e iterar.


## Qué hice
<!-- ✏️ Completado por Claude a partir de la sesión; cámbialo con tus palabras si quieres. -->
- Recorrí los 4 bloques de la lección con micro ejercicios: historia de la IA, funcionamiento interno de un LLM, casos de uso y límites.
- Relacioné los conceptos con backend: `for`+`await` vs `Promise.all` (RNN vs Transformer, decode vs prefill), costo por token, TTFT y streaming.
- Escribí el assignment en inglés (~295 palabras), iterando con correcciones: asistente de turnos por WhatsApp para pequeños negocios.
- Retomé la lección desde cero el 2026-09-26 tras la pausa por las lecciones 09 y 18 (créditos de Azure).

## Código y ejercicios
- `assignment.md` — mi startup de IA: asistente de turnos por WhatsApp (Problem / How I would use AI / Impact). Idea técnica clave: la IA conversa, pero la disponibilidad sale del calendario real vía API y la reserva se guarda en la base de datos (sin turnos inventados ni dobles reservas).

## Dudas pendientes
- [ ] 

## Resumen en una frase
Un LLM es un Transformer que predice el siguiente token en bucle: procesa la entrada en paralelo (prefill), genera la salida de a un token (decode) y elige cada token con probabilidades y temperatura; por eso no es determinista ni siempre correcto, y hay que validar lo que produce.

### Resumen extendido (con mis palabras, corregido ✏️)
En esta lección aprendí la evolución de la inteligencia artificial, desde la IA basada en reglas hasta los Transformers. Vi la diferencia entre RNN y Transformer y cómo se comparan en tiempo y memoria: la RNN es secuencial (tiempo lineal), el Transformer es paralelo pero su memoria crece de forma cuadrática.

Aprendí qué es tokenizar y por qué un token de salida cuesta más que uno de entrada: la entrada se procesa en una sola pasada en paralelo (*prefill*) y la salida necesita una pasada por token (*decode*). También entendí la temperatura, un parámetro que antes no lograba entender: una temperatura baja da respuestas más predecibles, pero **no garantiza que sean correctas**; una temperatura alta da más creatividad, al punto de elegir opciones muy poco probables (como "unicornio").

Vi los tipos de prompt: una instrucción en imperativo puede llevar implícita una pregunta. Es importante diferenciar la **instrucción** (qué hacer) de los **datos** (sobre qué hacerlo).

Por último, vi los límites de los LLMs: el **modelo** (no el prompt) puede alucinar, sobre todo con datos poco frecuentes en su entrenamiento o posteriores a su *knowledge cutoff*. Y lo más relevante para mí: no son deterministas, es decir, un mismo prompt puede dar dos salidas distintas.


