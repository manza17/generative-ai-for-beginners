# Repaso — Lección 01: Introducción a la IA generativa y los LLMs

> Sesiones del 2026-09-23 y del 26 al 28 de septiembre de 2026. Lección teórica, sin código del curso.
> Notas propias: [`notas.md`](notas.md) · Assignment: [`assignment.md`](assignment.md)

## 1. Qué hicimos, en orden
1. **Bloque 1: de dónde viene la IA generativa.** IA ⊃ ML ⊃ DL ⊃ GenAI, y el salto de RNN a Transformer.
2. **Bloque 2: cómo funciona un LLM.** Tokens → predicción del siguiente token → sampling con temperatura, en bucle.
3. **Bloque 3: para qué sirve.** Prompt y completion; tipos de prompt; instrucción frente a datos.
4. **Bloque 4: sus límites.** Alucinaciones, *knowledge cutoff* y no-determinismo.
5. **Knowledge check del README:** respondido correctamente (opción 3).
6. **Assignment en inglés:** una startup de turnos por WhatsApp, escrita en 3 secciones con varias rondas de corrección.

## 2. Conceptos, con analogías de backend

### IA ⊃ ML ⊃ DL ⊃ GenAI
- **IA con reglas:** `if "gratis" in asunto: spam = True`. Se rompe con "gr4tis".
- **ML:** aprende las señales a partir de correos etiquetados.
- **GenAI:** además de clasificar, **redacta** contenido nuevo.
- Clasificar tickets **no** es GenAI. Enviar una plantilla fija tampoco. Para clasificar alcanza con un modelo de ML clásico, que es más barato.

### RNN vs Transformer
```ts
// RNN: secuencial — cada paso espera al anterior
for (const palabra of texto) estado = await procesar(palabra, estado);

// Transformer: en paralelo — todas las palabras a la vez
await Promise.all(texto.map(p => procesar(p, texto)));
```
- El Transformer **no hace menos trabajo**; hace el trabajo **en paralelo**, y así aprovecha los miles de núcleos de la GPU.
- **Atención:** relaciona cualquier palabra con cualquier otra, sin importar la distancia entre ellas.
- **Costo:** la memoria crece de forma **cuadrática** (n²). Con el doble de texto hace falta 4 veces más memoria; con el triple, 9 veces más. De ahí los límites de contexto.
- La RNN, en cambio, crece de forma **lineal** en tiempo: con el doble de texto, tarda el doble.

### Tokens
- El modelo no ve palabras, ve **IDs de tokens**. 1 token ≈ 4 caracteres en inglés.
- El token es la unidad de **costo** y de **contexto**. En español se gastan más tokens que en inglés.
- Los espacios también cuentan: minificar el JSON o enviar **solo los campos necesarios** abarata la llamada.

### El ciclo completo de un LLM
```ts
let tokens = tokenizar(prompt);            // B: una sola vez → prefill
while (true) {
  const probs = modelo.predecir(tokens);   // D: probabilidades del siguiente token
  const siguiente = sortear(probs, temp);  // A: sorteo según la temperatura
  tokens.push(siguiente);                  // C: la salida se convierte en entrada
}                                          // D → A → C por cada token → decode
```
- ***Prefill:*** todo el prompt en **una sola pasada**, en paralelo.
- ***Decode:*** **una pasada por cada token** de salida, de forma secuencial. Por eso la salida es **más cara** (en `gpt-5-nano`, $0,40 frente a $0,05 por millón de tokens) y más lenta.
- **KV cache:** evita recalcular los tokens anteriores, pero no permite paralelizar el *decode*.

### Cuello de botella, TTFT y tokens/s
- **Cuello de botella:** la parte más lenta de un proceso, la que limita el total. Primero se **mide**, después se optimiza.
- **TTFT** (*Time To First Token*): lo domina el *prefill* y crece con el largo del **prompt**. El usuario ve una pantalla en blanco.
- **Tokens/s:** lo domina el *decode*. El tiempo total crece con el largo de la **respuesta**. Se mitiga con **streaming**.
- **El largo del bucle depende de la respuesta, no del documento.** Un resumen de 5 viñetas de un documento de 50.000 tokens son unas 150 vueltas.

### Probabilidades y temperatura
- El modelo calcula una **distribución de probabilidad** sobre todo su vocabulario y después **sortea** (*sampling*). Por eso no es determinista.
- **Temperatura baja:** resultados predecibles, útil para extraer datos. **Alta:** más creatividad y más errores.
- ⚠️ La temperatura baja reduce la **variabilidad**, no los **errores**: el token más probable también puede estar mal. La precisión se consigue **validando**: esquemas, código y revisión humana.
- Los modelos de razonamiento (`gpt-5-mini`) solo aceptan `temperature = 1`.

### Prompt y completion
- **Prompt** = entrada. **Completion** = salida generada.
- Tipos de prompt: instrucción, pregunta, texto a completar y código. Se pueden combinar.
- Hay que separar la **instrucción** (qué hacer) de los **datos** (sobre qué hacerlo). Es la base de la lección 04.

### Alucinaciones y límites
- El modelo optimiza lo **plausible**, no lo **verdadero**.
- Alucina más cuando el dato fue **poco frecuente en su entrenamiento**: la distribución queda plana y el sorteo elige algo inventado. El problema **no es el vocabulario**, que tiene todos los tokens necesarios.
- ***Knowledge cutoff:*** no sabe nada posterior a la fecha de su entrenamiento, y aun así responde con seguridad.
- **Mitigación:** darle los datos dentro del prompt (**RAG**, lección 15; **herramientas**, lección 11) y validar.
- Las **cuentas** las debe hacer el código: los números se tokenizan de forma irregular.
- Úsalo como un **primer borrador muy rápido** que luego validas e iteras.

## 3. Gotchas y confusiones de esta lección
| Confusión | Corrección |
|---|---|
| "El Transformer procesa menos palabras que la RNN" | Procesan las mismas palabras. La diferencia es el **paralelismo**. |
| "El Transformer ocupa menos memoria" | Ocupa **más**, porque crece en n². |
| "Con un documento largo, el cuello de botella es el *decode*" | Si la respuesta es corta, el cuello de botella es el ***prefill***, que se nota en el TTFT. El bucle depende de la **respuesta**. |
| "Alucina porque el dato no está en su vocabulario" | Es por la **frecuencia en los datos de entrenamiento**, no por el vocabulario. |
| "Temperatura baja = respuesta correcta" | Temperatura baja = respuesta **consistente**. Puede ser consistentemente incorrecta. |
| Orden del ciclo B–C–A–D | El orden correcto es **B → D → A → C**: no se puede añadir un token que todavía no se ha elegido. |

## 4. Assignment: lo técnico y lo del inglés
**Idea:** un asistente de turnos por WhatsApp para pequeños negocios.
- **La IA conversa**: entiende "el viernes por la tarde".
- **El código gestiona los datos críticos:**
  - la disponibilidad sale del **calendario real vía API**, así no hay turnos inventados;
  - la reserva se guarda en la **base de datos**, así no hay dobles reservas (*race condition*).
- **Las reglas del negocio** van en el system prompt. **No hace falta RAG** para media página de políticas.

**Mis patrones de error en inglés:**
1. **Plurales:** `customer` → `customers`.
2. **Calcos del español:** `disponible` → `available`; `for no answer` → `because they don't reply`; `response` como verbo → `respond to` / `answer`.
3. **Sujeto y objeto obligatorios:** `that it is`, `saves it`, `hire a receptionist`.
4. **`-s` de la tercera persona:** `the assistant answers / checks`.
5. **Posesivos:** `its` (para *business*) y `his` (para *owner*), no `your`.

También: el adjetivo va antes del sustantivo (`available time slots`); después de una preposición, el verbo va en *-ing* (`without making up`); `never` va después del verbo modal (`can never`).

## 5. Preguntas de autoevaluación
1. ¿Por qué el Transformer se entrena más rápido que una RNN, si procesan la misma cantidad de palabras? ¿Qué paga a cambio?
2. Un chatbot "tarda en empezar a responder" con PDFs largos, pero luego escribe rápido. ¿Qué fase es el cuello de botella y qué métrica lo mide?
3. ¿Por qué los tokens de salida cuestan más que los de entrada?
4. Extraes montos de facturas con temperatura 0 y el modelo devuelve siempre 1.250 cuando en la factura pone 1.520. ¿Por qué ocurre y cómo lo detectarías?
5. En tu startup de turnos, ¿qué hace la IA y qué **no** debe hacer nunca? ¿Por qué?
