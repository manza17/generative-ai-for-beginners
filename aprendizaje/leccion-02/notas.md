# Lección 02 — Explorar y comparar LLMs

**Inicio:** 2026-09-29
**Lenguaje(s):** — (lección teórica, sin código)

## Objetivos
- Elegir el modelo adecuado para cada caso de uso.
- Saber cómo probar, comparar e iterar modelos.
- Conocer las 4 formas de mejorar los resultados de un LLM, de la más barata a la más cara.

## Conceptos (con mis palabras)
- **Supervisado / no supervisado / auto-supervisado / refuerzo:** supervisado aprende con etiquetas puestas por personas; no supervisado descubre patrones sin etiquetas; **auto-supervisado** crea sus propias etiquetas ocultando parte de los datos y aprendiendo a predecirla (así se entrenan los LLMs: la etiqueta es el siguiente token); por refuerzo aprende con recompensas y castigos (RLHF ajusta los chatbots con calificaciones humanas).
  - Ejemplo auto-supervisado: entrenar un modelo que complete código tomando millones de archivos de GitHub, ocultando la última línea de cada función y haciendo que la prediga. La etiqueta (la última línea) ya estaba en el archivo: nadie etiquetó nada.
- **Coseno vs euclidiana:** el coseno mide el ángulo (dirección = significado, estándar en embeddings); la euclidiana mide la distancia en línea recta. Con vectores normalizados a largo 1, ordenan igual.
- **Foundation model vs LLM:** un *foundation model* se entrena de forma auto-supervisada con muchísimos datos, es muy grande y sirve de base para otros modelos (vía fine-tuning). Un LLM es un *foundation model* especializado en **texto**; hay otros de imagen, audio o multimodales (ej.: CLIP, imagen + texto). Ejemplo propio: `gpt-4.1-nano` (foundation) → `elements-limerick` (mi fine-tune de la lección 18).
- **Open-weight vs propietario:** open-weight = pesos descargables (Llama, Mistral; ojo con la licencia), lo ejecuto yo y los datos no salen de mi equipo, pero opero y mantengo la infraestructura. Propietario = solo por API (GPT, Gemini, Claude), más calidad y comodidad, pero dependo del proveedor y pago por token. Con open-weight gano **control**; con propietario, **comodidad y calidad**.
- **Encoder / decoder / encoder-decoder:** encoder-only (BERT) entiende pero no genera → clasificar, buscar, embeddings. Decoder-only (GPT, Llama) genera token a token → chat, redacción; es la arquitectura de casi todos los LLMs actuales. Encoder-decoder (T5, BART) entiende la entrada y genera otra → traducir, resumir. Para clasificar tickets: BERT (más chico, barato, devuelve una categoría y no alucina).
- **Servicio vs modelo vs deployment:** el modelo es el artefacto (pesos, arquitectura, tokenizer: `gpt-5-mini`); el servicio es el producto cloud que lo envuelve con infraestructura, seguridad, filtros y facturación (Azure OpenAI en Foundry); el deployment es mi instancia del modelo dentro del servicio, y **su nombre** es el que va en el código (`AZURE_OPENAI_DEPLOYMENT`). En la lección 00 coincidía con el del modelo porque acepté el nombre sugerido, pero podría haberse llamado distinto.
- **Resumen del bloque 1:** los modelos se clasifican por cómo se entrenan (*foundation model*: auto-supervisado y base de otros), por acceso (open-weight: control; propietario: comodidad y calidad), por arquitectura (encoder entiende, decoder genera, encoder-decoder transforma) y por cómo se consumen (modelo vs servicio); elegir bien depende de la tarea, los datos, el costo y las restricciones.
- **Cómo elegir un modelo (3 filtros):** la *model card* descarta (modalidades, contexto, licencia, regiones, acceso); los benchmarks comparan (solo si miden algo parecido a mi tarea); **mis propios datos deciden**: un set de prueba con casos reales y criterios medibles (precisión, function calling, TTFT, costo por conversación). Ejemplo propio: lección 09, `gpt-image-1-mini` descartado por *limited access*.
- **Antes de pasar a producción un cambio de modelo** (el código y el `.env` no cambian, pero el comportamiento sí):
  1. **Evaluar con mi set de prueba:** pasar el modelo anterior y el nuevo por los mismos 20–50 casos reales y comparar con criterios medibles:
     - **Precisión:** % de pedidos que el modelo interpreta bien (ej.: "el juevs a la tardecita" → jueves por la tarde).
     - **Function calling:** % de veces que llama a la función correcta (ej.: la API del calendario) con los parámetros correctos.
     - **TTFT** (*Time To First Token*): cuánto espera el usuario hasta ver el primer token de la respuesta; lo domina el *prefill*.
     - **Costo:** $ por conversación completa (tokens de entrada + salida × precio del modelo).
  2. **Revisar los parámetros:** que el modelo nuevo acepte los mismos (ej.: los de razonamiento no aceptan `temperature`).
  3. **Rollout gradual:** desviar primero un porcentaje chico del tráfico al modelo nuevo y completar el cambio solo si las métricas aguantan.
  - Ejemplo: el nuevo acierta 95 % vs 90 %, pero el TTFT pasa de 0,8 s a 3 s → no hay respuesta universal; se hace un **balance según el contexto**. En WhatsApp (asíncrono) 3 s pueden ser aceptables a cambio de la mitad de errores; en un asistente de voz, no.
- **Cómo mejorar resultados (4 escalones, de menor a mayor costo):** 1) prompt con contexto, 2) RAG, 3) fine-tuning, 4) entrenar desde cero. Los escalones 1 y 2 no tocan el modelo, solo lo que le doy; el 3 y el 4 crean un modelo nuevo. Empezar siempre por el 1.
- **Zero / one / few-shot:** instrucción sin ejemplos / con uno / con varios. Few-shot = costo **variable** (tokens extra en cada llamada: con 50 mensajes al día son ~2 centavos al mes). Fine-tuning = costo **fijo** (hosting por hora, ~$700–1.400 al mes en Standard) más el entrenamiento. El fine-tuning conviene con **millones de llamadas al día** (equilibrio ≈ 3 M/día), cuando los ejemplos no caben en el prompt o cuando la latencia es crítica. Antes de decidir: **hacer la cuenta completa**.
- **RAG:** antes de llamar al modelo, busco (*retrieval*) los fragmentos relevantes —con embeddings y una base vectorial, por significado— y los agrego al prompt (*augmented*) para que responda en base a ellos (*generation*). Sirve para datos privados o posteriores al *knowledge cutoff*; si los datos cambian, actualizo la base, no reentreno.
- **Cuándo usar RAG:** cuando el material **no cabe** en el prompt (o es caro enviarlo entero en cada llamada), p. ej. un catálogo de 3.000 productos. Si cabe (las políticas de la peluquería, media página), va directo en el system prompt. Que la información sea privada o única no alcanza por sí solo: lo que decide es el tamaño.
- **Fine-tuning:** crea un modelo nuevo ajustando pesos con pares entrada/salida. Conviene para: modelo chico especializado (barato y rápido), latencia (prompts cortos) y comportamiento estable (formato, tono, estilo) con muchos ejemplos buenos. **No** sirve para hechos que cambian o son privados (eso es RAG). Regla: **fine-tuning = cómo hablar; RAG = de qué hablar.** Ejemplo propio: lección 18, aprendió el formato del limerick, no a ser más preciso.
- **Ejercicio de repaso — ¿few-shot, RAG o fine-tuning?**

  | Caso | Elección | Por qué |
  |---|---|---|
  | (a) Chatbot sobre las políticas de RR. HH. de una empresa de 5.000 empleados: 200 páginas que se actualizan cada trimestre | **RAG** | 200 páginas no caben en el prompt y cambian cada trimestre; con fine-tuning habría que reentrenar cada vez. |
  | (b) Sistema con 2 millones de mensajes por día que siempre responde en un JSON de formato fijo y tono formal; hay 10.000 ejemplos buenos | **Fine-tuning** | Cumple las tres razones: volumen enorme, formato y tono estables, muchos ejemplos buenos. (Para el JSON, probar primero *structured outputs*; el fine-tuning sigue compensando por el tono y el costo a esa escala.) |
  | (c) Mi asistente de turnos, que debe sonar amable y cercano como mi amigo el peluquero | **Few-shot** | Bajo volumen y un tono que se transmite con pocos ejemplos; incluso podría alcanzar con describir el tono en el system prompt, sin ejemplos. |
- **Entrenar desde cero:** construir un *foundation model* propio; requiere billones de tokens, equipos especializados, miles de GPUs y millones de dólares. Solo tiene sentido con un dominio muy específico y datos gigantescos. Para el 99 % de los casos alcanza con los escalones 1 a 3.
- **Knowledge check del README — ¿qué enfoque mejora los resultados de un LLM: prompt con contexto, RAG o fine-tuning?** Las **tres** ayudan, según el caso: empezar siempre por el prompt con contexto (lo más barato y rápido de probar); RAG cuando faltan datos actuales o privados; fine-tuning cuando hace falta un formato, tono o patrón estable y hay muchos ejemplos buenos. Mi primera respuesta fue RAG (enriquece la respuesta con información actualizada sin la rigidez del fine-tuning), pero no hay un enfoque ganador: **depende del problema**. Ojo: RAG **es** dar contexto en el prompt (buscado automáticamente), no algo "más robusto"; si la búsqueda trae fragmentos equivocados, el modelo responde mal con total seguridad.
- **Resumen del bloque 3:** para mejorar un LLM se empieza por el prompt, se sube a RAG si faltan datos, a fine-tuning si hace falta un comportamiento estable a escala, y casi nunca se entrena desde cero.

## Qué hice
<!-- ✏️ Completado por Claude a partir de la sesión; cámbialo con tus palabras si quieres. -->
- Repasé los conocimientos previos (tipos de aprendizaje, distancias entre vectores) y conecté lo de la diplomatura (normalización, PEAS) con la lección.
- Recorrí los 3 bloques con micro ejercicios: clasificación de modelos, cómo compararlos y los 4 escalones para mejorar resultados.
- Hice la cuenta de costos few-shot vs fine-tuning para mi asistente de turnos: con 50 mensajes al día, few-shot cuesta ~2 centavos al mes y un fine-tune en Standard ~$700–1.400.

## Código y ejercicios
- Lección teórica, sin código. Ejercicios de repaso incluidos en "Conceptos" (few-shot / RAG / fine-tuning y knowledge check).

## Dudas pendientes
- [x] Challenge leído (ver "Documentación recomendada" abajo): leer sobre RAG en Azure AI Search aplicado a mi negocio (https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview). Se ve a fondo en las lecciones 08 y 15.

## Resumen en una frase

Elegir un LLM es filtrar por tarea, costo y restricciones y validar con mis propios datos; y para mejorarlo se sube por la escalera prompt → RAG → fine-tuning → entrenar desde cero, solo cuando el escalón anterior no alcanza.

### Resumen extendido (con mis palabras, corregido ✏️)
En esta lección aprendí cómo elegir un modelo y un concepto nuevo: el aprendizaje auto-supervisado, donde el entrenamiento oculta parte de los datos y el modelo aprende a predecirla, así que las etiquetas salen de los propios datos.
> ✏️ Antes decía "el modelo esconde etiquetas para predecirlas": quien oculta los datos es el **proceso de entrenamiento**; el modelo solo aprende a predecir lo oculto (por ejemplo, el siguiente token).

También vi la diferencia entre *foundation model* y LLM: están relacionados, y el concepto clave es que un LLM es un *foundation model* especializado en texto.

Sobre las arquitecturas: el encoder entiende (clasificar, buscar, embeddings), el decoder genera token a token y el encoder-decoder entiende la entrada y genera otra (traducir, resumir). Hoy casi todos los LLMs son decoder-only.
> ✏️ Antes decía "hoy en día alcanza con decoder": para **generar** sí, pero los encoders siguen usándose para clasificar y crear embeddings porque son más chicos y baratos (los modelos de embeddings de la lección 08 son de ese tipo).

Para elegir un modelo: la *model card* descarta, los benchmarks comparan y mis propios datos deciden.

El concepto más grande que me llevo son los 4 escalones para mejorar resultados, de menor a mayor costo: prompt con contexto, RAG, fine-tuning y entrenar desde cero, haciendo siempre la cuenta completa de costos antes de subir de escalón.
> ✏️ Agregados el párrafo de cómo elegir un modelo (era uno de los objetivos de la lección) y la idea de "hacer la cuenta completa", que fue el aprendizaje del ejercicio de costos.

## Documentación recomendada - learning
- RAG no reemplaza al LLM: le proporciona información relevante para que el LLM pueda generar una respuesta basada en datos externos.
- Azure AI Search es principalmente la capa de recuperación, no el modelo que genera la respuesta.
- En Agentic retrieval El LLM puede entender la pregunta, dividirla en subconsultas y ejecutarlas en paralelo.

Pregunta compleja
       ↓
      LLM
       ↓
divide la pregunta
       ↓
 ┌─────┼─────┐
 ↓     ↓     ↓
Q1    Q2    Q3
 ↓     ↓     ↓
Search Search Search
 └─────┼─────┘
       ↓
  mejores resultados
       ↓
      LLM
       ↓
    respuesta

Por ejemplo: 
** "¿Cuál es la política de vacaciones para empleados remotos contratados después de 2023?" **
Puede convertirse en: 
Q1 → política de vacaciones
Q2 → empleados remotos
Q3 → contrataciones posteriores a 2023

## ---------------- Mapa mental ---------------------

RAG
│
├── 1. PREPARAR DATOS
│      ├── documentos
│      ├── chunking
│      └── embeddings
│
├── 2. INDEXAR
│      └── Azure AI Search
│
├── 3. RECUPERAR
│      ├── keyword
│      ├── vector
│      └── hybrid ⭐
│
├── 4. RANKING
│      └── semantic ranking
│
└── 5. GENERAR
       └── LLM

RAG CLÁSICO
Pregunta
   ↓
Search
   ↓
Resultados
   ↓
LLM


AGENTIC RAG
Pregunta
   ↓
LLM analiza
   ↓
Subconsultas
   ↓
Search
   ↓
Resultados
   ↓
LLM
   ↓
Respuesta