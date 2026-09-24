# Repaso — Lección 18: Fine-tuning

> Sesión del 2026-09-23/24. Hecha fuera de orden (laboratorio por vencimiento de créditos de Azure).
> Código: [`python/oai-assignment.ipynb`](python/oai-assignment.ipynb) · Notas propias: [`notas.md`](notas.md)

## 1. Qué hicimos, en orden

1. **Decidimos modelo y tier, priorizando coste** (verificado en la documentación de Microsoft):
   - Modelo base **`gpt-4.1-nano`**, el más barato con fine-tuning (el notebook usaba `gpt-4.1-mini`).
   - Entrenamiento **`developerTier`**: usa capacidad ociosa, por eso es más barato, pero sin SLA. Si se queda en `pending` mucho tiempo, la alternativa es `GlobalStandard`.
   - Deployment **Developer Tier**: sin cargo por hora. Nunca Standard para un fine-tune, porque cobra por hora aunque no se use.
     - **Qué se sacrifica:** no hay SLA de disponibilidad ni garantía de rendimiento (latencia variable, menor prioridad frente al tráfico de pago) y no está pensado para escalar. Microsoft lo define como un tier para **evaluar modelos candidatos, no para producción**.
2. **Subimos los datos** con `client.files.create`: 10 ejemplos de entrenamiento y 5 de validación. Azure exige un mínimo de 10 para entrenar.
3. **Esperamos a que los archivos quedaran en `processed`** antes de crear el job.
4. **Creamos el job:** `ftjob-f21e5661...`. Terminó rápido: 100 steps y 8000 tokens facturados.
5. **Leímos las métricas** y detectamos **overfitting**. Elegimos **ckpt-step-80**.
6. **Desplegamos en el portal:** Fine-tuning → job → **Checkpoints** → `ckpt-step-80` → **Deploy** → tipo **Developer** → nombre `elements-limerick`. Esperamos a que el estado pasara de *Creating* a *Succeeded*.
7. **Probamos** con el system del entrenamiento y con el del notebook, y comparamos las salidas.

## 2. El código, celda por celda

> VS Code no numera las celdas. El `[n]` a la izquierda es el **orden de ejecución**, no la posición. Por eso aquí las identifico por su primera línea.

### `import os ...`: cliente y subida de archivos
```python
client = OpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    base_url=f"{os.environ['AZURE_OPENAI_ENDPOINT'].rstrip('/')}/openai/v1/",
)
training_response = client.files.create(file=open("./training-data.jsonl", "rb"), purpose="fine-tune")
validation_response = client.files.create(file=open("./validation-data.jsonl", "rb"), purpose="fine-tune")
```
- Usa el cliente `OpenAI` normal, no `AzureOpenAI`, apuntado a `/openai/v1/`: la API de Azure compatible con OpenAI. Con ella no hace falta `api_version`.
- `.rstrip('/')` evita que quede `//` en la URL, porque el endpoint termina en `/`.
- `"rb"` abre en binario. `purpose="fine-tune"` hace que Azure valide el archivo como dataset.
- A partir de aquí los archivos se referencian por su **id** (`file-...`), no por la ruta local.
- ⚠️ Si vuelves a ejecutar esta celda, **sube los archivos otra vez** y obtienes ids nuevos. Nos pasó: quedaron 4 archivos.

### Celda agregada: comprobar que los archivos están procesados
```python
for fid in (training_file_id, validation_file_id):
    f = client.files.retrieve(fid)
    print(fid, "->", f.status)
```
- Subir no es lo mismo que tener listo. Azure importa y valida el archivo en segundo plano: `pending` → `running` → `processed`, o `error` si el formato es inválido.

### `# Create the fine-tuning job.`
```python
job = client.fine_tuning.jobs.create(
    model="gpt-4.1-nano-2025-04-14",
    training_file=training_file_id,
    validation_file=validation_file_id,
    suffix="elements-limerick",
    seed=105,
    extra_body={"trainingType": "developerTier"},
)
```
- `model`: el modelo base, con **versión explícita**, como en la documentación.
- `validation_file`: permite medir `valid_loss` con ejemplos que el modelo no usa para entrenar.
- `suffix`: se añade al nombre del modelo resultante para reconocerlo.
- `seed`: hace el entrenamiento reproducible.
- `extra_body`: el SDK de OpenAI no conoce `trainingType` porque es exclusivo de Azure, y `extra_body` lo añade tal cual al JSON de la petición. El SDK valida los *nombres* de los parámetros que conoce; el *valor* lo valida el servidor.

### `# List the last 10 fine-tuning jobs` / `# Track progress...`
- `jobs.list_events(job_id)` devuelve los eventos del job: validación, cola, métricas por step y final.
- La primera celda muestra el objeto sin formato (`SyncCursorPage[...]`). La de `# Track progress...` imprime solo los mensajes, de forma legible.

### `# When the job finishes, the last few epochs are available...`
```python
checkpoints = client.fine_tuning.jobs.checkpoints.list(job_id)
```
- Lista los checkpoints que se pueden desplegar. Azure solo guarda los **3 últimos** (en nuestro caso, los steps 80, 90 y 100).

### `# Once deployed, call your fine-tuned model...`
```python
completion = client.responses.create(
    model="elements-limerick",   # nombre del DEPLOYMENT
    input=[
        {"role": "system", "content": "Elle is a factual chatbot that answers questions about elements in the periodic table with a limerick"},
        {"role": "user", "content": "Tell me about Strontium"},
    ],
    store=False,
)
print(completion.output_text)
```
- `input` es la lista de mensajes del prompt. `system` fija el comportamiento y `user` es la pregunta.
- Cambiamos el system para que coincidiera **exactamente** con el de los datos de entrenamiento. El notebook traía `"You are Elle, a ..."`.
- `store=False` indica a Azure que no guarde la conversación.

## 3. Las métricas y el overfitting

| Step | train_loss | full_valid_loss |
|---|---|---|
| 50 | 0.082 | **2.10** |
| 60 | 0.039 | 2.27 |
| 70 | 0.015 | 2.50 |
| 80 | 0.231 | 2.50 |
| 90 | 0.003 | 2.63 |
| 100 | 0.007 | 2.68 |

- **Loss** mide cuánto se equivoca el modelo. `train_loss` se calcula sobre los ejemplos de entrenamiento; `valid_loss`, sobre ejemplos que **no ve** al entrenar.
- Aquí `train_loss` cae a ~0 (con *accuracy* de 1: reproduce los ejemplos token a token) mientras `valid_loss` **sube**. Eso es **overfitting**: con 10 ejemplos, el modelo los memorizó en vez de aprender el patrón general.
- Remedios: **más datos** (lo que más ayuda), menos épocas (`hyperparameters={"n_epochs": ...}`) o menor learning rate.
- **Validación vs prueba:** la validación se usa *durante* el proceso para decidir cosas como qué checkpoint desplegar. La prueba se reserva para la medición final.
- Elegimos **ckpt-step-80**, el de menor `valid_loss` entre los disponibles. Con solo 5 ejemplos de validación, las diferencias tienen mucho ruido.

## 4. Resultados

| System | Salida |
|---|---|
| `Elle is a ...` (el del entrenamiento) | *Strontium, a metal so fair, - In fireworks it gives color to spare, - It's in? - In bones, you see - So, strong and in skeletons, it's there* |
| `You are Elle, a ...` (el del notebook) | *Strontium, a metal so fair - In fireworks, it gives fire a red flare - In magnets, it's a part - And in bones, it's a start - So in your body, it's quite rare* |

- **Lo que aprendió:** el **formato**, es decir, 5 versos separados por ` - ` y rima tipo limerick. Un modelo base no produce ese separador por su cuenta.
- **Lo que no garantiza:** la calidad. Aparecen versos rotos (`It's in?`) e imprecisiones que se aceptan con tal de que rime.
- **Comparación de system:** con un cambio menor en el system, el formato se mantuvo. Con **una sola muestra por caso** no se puede concluir cuál es mejor, porque el modelo no es determinista. La buena práctica sigue siendo usar el mismo system del entrenamiento.

## 5. Gotchas de esta sesión
| Error | Causa | Solución |
|---|---|---|
| `400 invalidPayload: The fineTuningJob field is required` | `trainingType: "Developer"` (nombre del portal) no es un valor que acepte la API. Al no poder interpretar el JSON, Azure descarta el body completo. | Usar `"developerTier"`. |
| `400: The specified file reference must point to a completed file import` | Se creó el job antes de que los archivos terminaran de procesarse. | Esperar a que `files.retrieve(id).status == "processed"`. |
| Llamar al deployment mientras dice *Creating* | El deployment todavía no existe para la API. | Esperar a *Succeeded*; si no, da `404 DeploymentNotFound`. |
| Archivos duplicados | Se volvió a ejecutar la celda de subida. | No repetir esa celda; reutilizar los ids. |

## 6. Preguntas de autoevaluación
1. `train_loss` baja y `valid_loss` sube. ¿Qué está pasando y qué tres cosas cambiarías?
2. ¿Qué diferencia hay entre el conjunto de validación y el de prueba?
3. ¿Por qué `trainingType` va en `extra_body` y no como parámetro normal? ¿Quién valida su valor?
4. ¿Por qué un fine-tune nunca debería quedar desplegado en Standard para experimentar?
5. ¿Qué aprende un modelo con fine-tuning de 10 ejemplos: formato, conocimiento o ambos? ¿Cómo lo comprobaste?
