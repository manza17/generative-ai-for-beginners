# Lección 18 — Fine-tuning

> Hecha fuera de orden por vencimiento de créditos. Repasar al llegar a las lecciones 04 y 06.

**Inicio:** 2026-09-23
**Lenguaje(s):** Python

## Objetivos
- Entender qué es el fine-tuning y cuándo conviene frente a un buen prompt.
- Ejecutar el ciclo completo en Foundry: subir datos → crear job → monitorear → desplegar → probar.
- Leer las métricas de entrenamiento (loss) para detectar overfitting y elegir un checkpoint.

## Conceptos (con mis palabras)
- **Loss:** mide cuánto se equivoca el modelo; mientras más bajo, mejor.
- **train_loss:** se calcula sobre los ejemplos con los que se entrena.
- **valid_loss:** se calcula sobre el conjunto de validación.
  > ✏️ La clave es que son ejemplos que el modelo **nunca ve** durante el entrenamiento; por eso miden si generaliza.
- **Overfitting:** el sobreajuste surge porque el modelo terminó memorizando en lugar de aprender el patrón general.
  > ✏️ Cómo se detecta: `train_loss` sigue bajando (llegó a ~0.003 y `train_mean_token_accuracy = 1`) mientras `valid_loss` sube (de 2.10 en el step 50 a 2.68 en el 100). Remedios: más ejemplos, menos épocas (`n_epochs`) o menor learning rate.
- **Conjunto de entrenamiento vs validación:** el de entrenamiento es el que se utiliza para entrenar el modelo, mientras que el de validación es para corroborar qué tan bien fue entrenado.
  > ✏️ Más preciso: la validación mide qué tan bien **generaliza** a datos nuevos y se usa para tomar decisiones durante el entrenamiento (qué checkpoint elegir). No confundir con el conjunto de **prueba**, que se reserva para medir el resultado final una sola vez.
- **ckpt-step-80:** se elige el checkpoint que predijo mejor.
  > ✏️ Concretamente: el de menor `full_valid_loss` (2.50) entre los disponibles. Azure solo guarda los **3 últimos** checkpoints (80, 90, 100); el step 50 era mejor pero ya no se podía desplegar.

## Qué hice
<!-- ✏️ Completado por Claude a partir de la sesión; revísalo y cámbialo con tus palabras si quieres. -->
- Fine-tuning de `gpt-4.1-nano-2025-04-14` con 10 ejemplos de limericks (5 de validación), entrenamiento `developerTier`: 8000 tokens facturados.
- Desplegué el checkpoint `ckpt-step-80` como `elements-limerick` en **Developer Tier** (sin costo por hora).
- Probé con "Tell me about Strontium": respetó el formato aprendido (5 versos separados por ` - `), con algún verso roto (`It's in?`).
- Comparé el system del entrenamiento (`Elle is a...`) con el del notebook (`You are Elle...`): ambos mantuvieron el formato. Con una muestra por caso no se puede concluir cuál es mejor.

## Código y ejercicios
- `python/oai-assignment.ipynb` — fine-tuning de gpt-4.1-nano (Developer) con limericks de elementos.

## Dudas pendientes
- [ ] 

## Resumen en una frase
