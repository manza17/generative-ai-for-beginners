# Lección 09 — Apps de generación de imágenes

> Hecha fuera de orden por vencimiento de créditos. Repasar al llegar a las lecciones 04 y 06.

**Inicio:** 2026-09-23
**Lenguaje(s):** Python

## Objetivos
- Desplegar un modelo de generación de imágenes en Foundry y llamarlo desde código.
- Entender cómo llega la imagen en la respuesta (base64) y cómo guardarla.
- Conocer los parámetros que controlan resultado y coste (`size`, `quality`, `n`).

## Conceptos (con mis palabras)
- **Base64:** JSON es un formato de texto y no admite bytes binarios, por lo cual se codifican en texto para que viajen dentro del JSON. A cambio, ocupan un 33 % más.
- **`finally` vs `else`:** cambié `finally` por `else` porque el bloque `finally` siempre se ejecuta, haya pasado algo o no. En cambio, el bloque `else` solo se ejecuta si no ocurrió un error. De paso, descomenté el bloque `except` para capturar el error.
  > ✏️ `except BadRequestError` captura solo los errores 400 (prompt rechazado por el filtro de contenido o parámetros inválidos). Un 401 (key mal) o un 404 (deployment inexistente) no entran ahí y muestran su traceback, que es lo que queremos para errores de configuración.
- **`size`:** es la resolución de la imagen; a más píxeles, más costo.
- **`quality`:** define la calidad. Si no se especifica, el modelo decide qué calidad usar y a veces utiliza alta, lo cual implica mayor costo. Este parámetro no venía en el código del curso: lo agregamos para abaratar (`'low'`).

## Qué hice
- Desplegué un modelo para generar imágenes (`gpt-image-2.5-flare`, Global Standard) y agregué su nombre de deployment al `.env` como `AZURE_OPENAI_IMAGE_DEPLOYMENT`, para usarlo en el código.
  > ✏️ Usamos una variable nueva porque `AZURE_OPENAI_DEPLOYMENT` ya apunta al modelo de chat (`gpt-5-mini`). Cada deployment es un modelo distinto y necesita su propio nombre.
- El procedimiento para generar la imagen es crear un cliente; ese cliente llama a la ruta de la API que genera imágenes (`client.images.generate`) con los parámetros descritos arriba en Conceptos. La API devuelve la imagen en base64 para que pueda viajar en el JSON. Luego decodifico ese base64 a bytes y lo guardo como PNG: esa es la imagen generada según el prompt que se pasó por parámetro en `generate`.
  > ✏️ Corrección: la API **no** devuelve una ruta ni una URL de la imagen, solo el base64 (`data[0].b64_json`). La ruta `images/generated-image.png` la arma el propio script en local (`image_path`) para guardar el archivo.
- Probé con otro prompt (un dachshund en lugar del conejo, con otro texto en la imagen).

## Código y ejercicios
- `python/aoai-app.py` — genera una imagen con `gpt-image-2.5-flare` a partir de un prompt, la decodifica de base64 y la guarda en `python/images/generated-image.png`.

## Dudas pendientes
- [ ] 

## Resumen en una frase
<!-- ✏️ Esta sección es para UNA frase propia que resuma la lección. Las viñetas que tenías aquí las moví a "Conceptos". -->
