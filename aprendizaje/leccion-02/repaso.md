# Repaso — Lección 02: Explorar y comparar LLMs

> Sesión del 2026-09-29. Lección teórica, sin código.
> Notas propias: [`notas.md`](notas.md)

## 1. Qué hicimos, en orden
1. **Conocimientos previos:** supervisado, no supervisado, auto-supervisado y por refuerzo; distancias coseno y euclidiana; normalización.
2. **Bloque 1: cómo se clasifican los modelos.** *Foundation model* frente a LLM, open-weight frente a propietario, arquitecturas y servicio frente a modelo.
3. **Bloque 2: cómo elegir un modelo.** *Model card* → benchmarks → evaluación con datos propios.
4. **Bloque 3: cómo mejorar los resultados.** Prompt → RAG → fine-tuning → entrenar desde cero, con la cuenta de costos real.
5. **Knowledge check del README:** "las tres ayudan, según el caso".

## 2. Conceptos clave

### Tipos de aprendizaje
| Tipo | Etiquetas | Ejemplo |
|---|---|---|
| Supervisado | Las pone una **persona** | Correos marcados como spam o no spam |
| No supervisado | **No hay** | Descubrir grupos de clientes |
| **Auto-supervisado** | Salen **de los propios datos** | Predecir el siguiente token; ocultar la última línea de una función y predecirla |
| Por refuerzo | Recompensas y castigos | RLHF: personas califican las respuestas del chatbot |

- Los LLMs se pre-entrenan de forma **auto-supervisada**. Por eso pudieron usar billones de tokens: etiquetar a mano habría sido imposible.

### Vectores
- **Coseno:** el ángulo entre vectores, es decir, la dirección, que representa el significado. Es el estándar en embeddings.
- **Euclidiana:** la distancia en línea recta.
- **Normalización:** con embeddings se deja cada vector con **largo 1** (normalización L2), y entonces coseno y euclidiana ordenan igual. No es lo mismo que el *min-max scaling* (llevar a 0–1), que se aplica a columnas de un dataset.

### Bloque 1: clasificación de modelos
- ***Foundation model:*** entrenado de forma auto-supervisada, muy grande y base de otros modelos. Un **LLM** es uno especializado en **texto**. **CLIP** (imagen + texto) es un *foundation model*, pero no un LLM.
  - Ejemplo propio: `gpt-4.1-nano` → `elements-limerick` (lección 18).
- **Open-weight frente a propietario:**

  | | Open-weight (Llama, Mistral) | Propietario (GPT, Gemini, Claude) |
  |---|---|---|
  | Acceso | Descargas los pesos, **ojo con la licencia** | Solo por API |
  | Datos | No salen de tu infraestructura | Viajan al proveedor |
  | Costo | Hardware y operación | Por token |
  | Ventaja | **Control** | **Comodidad y calidad** |

  - En un proyecto regulado (el caso del hospital), primero se lee la **regulación exacta**. Muchas exigen "en este país", no "en mis servidores", y un proveedor con residencia de datos puede servir.
- **Arquitecturas:**
  - **Encoder-only** (BERT): entiende → clasificar, buscar, embeddings. Para clasificar tickets: más pequeño, más barato y no alucina texto.
  - **Decoder-only** (GPT, Llama): genera token a token. Es la arquitectura de casi todos los LLMs actuales.
  - **Encoder-decoder** (T5, BART): transforma un texto en otro → traducir, resumir.
- **Servicio, modelo y deployment:**
  - **Modelo:** el artefacto (`gpt-5-mini`).
  - **Servicio:** el producto cloud (Azure OpenAI en Foundry).
  - **Deployment:** tu instancia del modelo dentro del servicio. **En el código va el nombre del deployment.** Funciona como capa de abstracción: puedes cambiar el modelo sin tocar el código, pero **hay que probar**, porque el comportamiento cambia.

### Bloque 2: cómo elegir un modelo
1. **Model card → descartar:** modalidades, contexto, licencia, regiones y acceso. Por ejemplo, `gpt-image-1-mini` quedó descartado en la lección 09 por *limited access*.
2. **Benchmarks → comparar:** solo si miden algo **parecido a tu tarea**. Un benchmark de programación no dice nada sobre un asistente de turnos.
3. **Tus datos → decidir:** un set de prueba con 20–50 casos reales y **criterios medibles**: precisión, *function calling*, TTFT y costo por conversación.
- Relación con **PEAS**: la medida de performance define **qué es el éxito**; los criterios de evaluación lo hacen **medible**.

### Bloque 3: la escalera para mejorar resultados
| # | Enfoque | Cambia el modelo | Costo |
|---|---|---|---|
| 1 | Prompt con contexto (zero/one/few-shot) | No | 💲 |
| 2 | RAG | No | 💲💲 |
| 3 | Fine-tuning | **Sí** | 💲💲💲 |
| 4 | Entrenar desde cero | **Sí** | 💲💲💲💲💲 |

- **Few-shot:** costo **variable**, porque repites los ejemplos en cada llamada. Esos ejemplos se procesan en el *prefill*, no se "itera" sobre ellos.
- **Fine-tuning:** costo **fijo**. El hosting en Standard se cobra **por hora**, aunque nadie lo use.
- **RAG:**
  - retrieval: buscar fragmentos por significado, con embeddings y una base vectorial
  - augmented: añadirlos al prompt
  - generation: el modelo responde en base a ellos
  - Se usa cuando el material **no cabe** en el prompt. Si los datos cambian, actualizas la base y no reentrenas.
- **Regla:** **fine-tuning = cómo hablar** (formato, tono); **RAG = de qué hablar** (hechos).
- **Entrenar desde cero:** billones de tokens y millones de dólares. Casi nunca es la respuesta.

### La cuenta de costos (asistente de turnos, 50 mensajes al día)
| Opción | Cálculo | Costo mensual |
|---|---|---|
| Few-shot | 300 tokens extra × 50 × 30 = 450.000 tokens × $0,05/M | **~$0,02** |
| Fine-tune en Standard | ~$1–2/hora × 730 horas | **~$700–1.400**, más el entrenamiento |

- **Punto de equilibrio:** ~$1.400 ÷ $0,05/M ≈ 28.000 M tokens al mes ÷ 300 ≈ **3 millones de llamadas al día**.
- El fine-tuning también conviene cuando los ejemplos no caben en el prompt o cuando la latencia es crítica.

### Ejercicio de repaso: ¿few-shot, RAG o fine-tuning?
| Caso | Elección | Por qué |
|---|---|---|
| Políticas de RR. HH.: 200 páginas que cambian cada trimestre | **RAG** | No caben en el prompt y cambian; con fine-tuning habría que reentrenar cada vez. |
| 2 M de mensajes al día, JSON fijo, tono formal, 10.000 ejemplos | **Fine-tuning** | Volumen, formato estable y muchos ejemplos. Para el JSON, probar antes *structured outputs*. |
| Tono amable del asistente de turnos | **Few-shot** | Bajo volumen. Incluso puede alcanzar con una instrucción en el system prompt. |

## 3. Gotchas y confusiones de esta lección
| Confusión | Corrección |
|---|---|
| "Auto-supervisado = no supervisado" | El auto-supervisado **sí** tiene etiquetas, pero salen de los propios datos. |
| "En `AZURE_OPENAI_DEPLOYMENT` iba el nombre del modelo" | Iba el nombre del **deployment**. Coincidía porque acepté el nombre que proponía el portal. |
| "Few-shot tiene que iterar sobre los ejemplos" | Los ejemplos son entrada y se procesan en el ***prefill***, en paralelo. El costo real está en **pagar esos tokens en cada llamada**. |
| "El fine-tune cobra ~$2 por millón de tokens" | El hosting en Standard se cobra **por hora**, aunque no se use. Hay que comparar costo variable con costo fijo. |
| "Fine-tuning conviene porque se paga una vez" (con 50 mensajes al día) | Con la cuenta completa, gana el few-shot por mucho: 2 centavos frente a cientos de dólares. |
| "Uso RAG porque la información es única del negocio" | Lo que decide es el **tamaño** (si cabe o no en el prompt), no que sea privada. |
| "RAG enriquece el modelo y es más robusto que el prompt" | RAG enriquece la **respuesta**, no el modelo, **y es** dar contexto en el prompt. Añade piezas que pueden fallar. |

## 4. Preguntas de autoevaluación
1. ¿Por qué los LLMs se pueden entrenar con billones de tokens sin etiquetado humano? ¿Cómo se llama ese tipo de aprendizaje?
2. Un hospital no puede sacar datos de sus servidores. ¿Open-weight o propietario? ¿Qué pierde a cambio?
3. El modelo A saca 92 % en un benchmark de código y el B, 85 %. ¿Qué haces antes de elegir para un chatbot de atención al cliente?
4. Con 50 mensajes al día, ¿few-shot o fine-tuning? Justifícalo **con números**.
5. ¿Qué enseña el fine-tuning y qué aporta RAG? Da un caso para cada uno.
