# Repaso — Lección 09: Apps de generación de imágenes

> Sesión del 2026-09-23/24. Hecha fuera de orden (laboratorio por vencimiento de créditos de Azure).
> Código: [`python/aoai-app.py`](python/aoai-app.py) · Notas propias: [`notas.md`](notas.md)

## 1. Qué hicimos, en orden

1. **Elegimos el modelo.** `gpt-image-1-mini` es el más barato, pero requiere solicitar acceso a Microsoft (*limited access*). Entre los disponibles sin solicitud, `gpt-image-2.5-flare` es el optimizado para coste y velocidad. DALL·E 3 está retirado para nuevos deployments.
2. **Desplegamos en el portal** (ai.azure.com → proyecto → modelo → flecha ▾ de **Deploy** → **Custom settings**):
   - Tipo **Global Standard**: en imágenes se paga por imagen generada, no por hora.
   - Nombre del deployment: `gpt-image-2.5-flare`.
   - *Default settings* despliega sin mostrar el tipo; por eso usamos *Custom settings*.
3. **Agregamos una variable al `.env`:** `AZURE_OPENAI_IMAGE_DEPLOYMENT`. El script original usaba `AZURE_OPENAI_DEPLOYMENT`, pero esa ya apunta al modelo de chat.
4. **Adaptamos la copia del script:** variable nueva, `quality='low'` y manejo de errores con `except` + `else`.
5. **Ejecutamos:** `pip install pillow` y luego `python aoai-app.py`. Generamos el conejo y, después, un dachshund con un prompt propio.

## 2. El código, bloque por bloque

### Cliente
```python
client = AzureOpenAI(
    api_key=os.environ['AZURE_OPENAI_API_KEY'],
    api_version="2025-04-01-preview",
    azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],
)
model = os.environ['AZURE_OPENAI_IMAGE_DEPLOYMENT']
```
- Es el mismo cliente de la prueba de humo (lección 00), con una `api_version` más nueva, porque la API de imágenes con `gpt-image` la requiere.
- `model` recibe el **nombre del deployment**, no el nombre del modelo. Azure busca un deployment con ese nombre dentro de tu recurso.

### Petición
```python
result = client.images.generate(
    model=model,
    prompt='Bunny on horse, holding a lollipop, ...',
    size='1024x1024',
    quality='low',
    n=1,
)
```
- `images.generate` llama a otra ruta de la API (`/images/generations`), distinta de `chat.completions`.
- `prompt`: la descripción de la imagen.
- `size`: la resolución. Más píxeles, más coste.
- `quality`: `low` / `medium` / `high`. Si no se indica, decide el modelo y puede elegir alta, que es más cara. **No venía en el original; lo agregamos.**
- `n`: cuántas imágenes generar. Cada una se cobra.

### Respuesta: base64 → archivo
```python
generation_response = json.loads(result.model_dump_json())
image_b64 = generation_response["data"][0]["b64_json"]
generated_image = base64.b64decode(image_b64)
with open(image_path, "wb") as image_file:
    image_file.write(generated_image)
```
- La API **no devuelve una URL ni una ruta**, sino la imagen codificada en **base64** dentro del JSON.
- Por qué base64: JSON es texto y no puede transportar bytes binarios, así que se codifican como texto. A cambio, ocupan ~33 % más.
- `model_dump_json()` + `json.loads` convierten la respuesta del SDK en un dict. Es un rodeo: `result.data[0].b64_json` da lo mismo.
- `b64decode` recupera los bytes del PNG. `"wb"` escribe en modo binario.
- La ruta `images/generated-image.png` la construye **el script**, no la API.

### Mostrar
```python
Image.open(image_path).show()
```
Pillow abre el PNG en el visor de imágenes del sistema.

### Manejo de errores
```python
try:
    ...
except BadRequestError as err:
    print("Petición rechazada:", err)
else:
    print("completed!")
```
- **Error del original:** el `except` estaba comentado y había un `finally`, así que imprimía `completed!` **incluso cuando fallaba**.
- `finally` se ejecuta **siempre**; sirve para limpiar recursos.
- `else` se ejecuta **solo si no hubo excepción**; sirve para lo que depende del éxito.
- `BadRequestError` es un **400**: prompt bloqueado por el **filtro de contenido** de Azure, o parámetros inválidos.
- Un 401 (key incorrecta) o un 404 (deployment inexistente) **no** se capturan a propósito: son errores de configuración y conviene ver el traceback completo.

## 3. Gotchas de esta sesión
- Separar las variables de entorno por deployment: chat e imagen son modelos distintos.
- Algunos modelos baratos requieren solicitar acceso (`gpt-image-1-mini`). Revisa el *Lifecycle* y el acceso antes de elegir.
- El texto dentro de las imágenes, como el "hello" del prompt, es lo que más suele fallar en estos modelos.
- El mismo prompt da imágenes distintas en cada ejecución: es no-determinismo, igual que en los LLMs de texto.
- `os.path.join(os.curdir, 'images')` es relativo al **directorio desde donde ejecutas** el script, no a la ubicación del script. Al ejecutarlo desde la raíz del repo, la imagen se guardó en la carpeta `images/` del curso original. Hay que ejecutarlo desde `aprendizaje/leccion-09/python/`, o construir la ruta con `os.path.dirname(__file__)`.

## 4. Preguntas de autoevaluación
1. ¿Por qué `model=` recibe el nombre del deployment y no el del modelo? ¿Qué error da si no coincide?
2. ¿Por qué la imagen viaja en base64? ¿Qué costo tiene?
3. ¿En qué se diferencian `finally` y `else` en un `try`? ¿Cuál usarías para cerrar una conexión?
4. Si el filtro de contenido bloquea tu prompt, ¿qué excepción recibes y qué código HTTP?
5. Nombra dos parámetros de `images.generate` que afectan al coste.
