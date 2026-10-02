# Progreso — Generative AI for Beginners

Estados: ⬜ Pendiente · 🟡 En curso · ✅ Terminada · ⏭️ Salteada

| #  | Lección                              | Estado | Inicio | Fin | Resumen en una línea |
|----|--------------------------------------|--------|--------|-----|----------------------|
| 00 | Course Setup                         | ✅     | 2026-09-23 | 2026-09-23 | Entorno de aprendizaje listo: CLAUDE.md, skills, plantillas y permisos |
| 01 | Introducción a GenAI y LLMs          | ✅     | 2026-09-23 | 2026-09-28 | Cómo funciona un LLM (tokens, prefill/decode, temperatura, alucinaciones) + assignment en inglés |
| 02 | Explorar y comparar LLMs             | ✅     | 2026-09-29 | 2026-09-29 | Tipos de modelos, cómo elegirlos y escalera prompt → RAG → fine-tuning → entrenar |
| 03 | Uso responsable de GenAI             | ✅     | 2026-10-01 | 2026-10-02 | 6 principios, 3 riesgos y ciclo medir → mitigar (4 capas) → operar, aplicado a Bartun |
| 04 | Fundamentos de Prompt Engineering    | ⬜     |        |     |                      |
| 05 | Prompts avanzados                    | ⬜     |        |     |                      |
| 06 | Apps de generación de texto          | ⬜     |        |     |                      |
| 07 | Apps de chat                         | ⬜     |        |     |                      |
| 08 | Apps de búsqueda                     | ⬜     |        |     |                      |
| 09 | Apps de generación de imágenes       | ✅     | 2026-09-23 | 2026-09-24 | Generación de imágenes con gpt-image-2.5-flare: base64, quality/size y manejo de errores |
| 10 | Apps low code                        | ⬜     |        |     |                      |
| 11 | Function calling                     | ⬜     |        |     |                      |
| 12 | UX para apps de IA                   | ⬜     |        |     |                      |
| 13 | Seguridad en apps de IA              | ⬜     |        |     |                      |
| 14 | Ciclo de vida de apps GenAI          | ⬜     |        |     |                      |
| 15 | RAG y bases de datos vectoriales     | ⬜     |        |     |                      |
| 16 | Modelos open source                  | ⬜     |        |     |                      |
| 17 | Agentes de IA                        | ⬜     |        |     |                      |
| 18 | Fine tuning                          | ✅     | 2026-09-23 | 2026-09-24 | Fine-tuning de gpt-4.1-nano (limericks): overfitting detectado, ckpt-step-80 en Developer Tier |
| 19 | Small Language Models                | ⬜     |        |     |                      |
| 20 | Modelos de Mistral                   | ⬜     |        |     |                      |
| 21 | Modelos de Meta                      | ⬜     |        |     |                      |

## Bitácora
<!-- Una línea por sesión: AAAA-MM-DD — qué hice — qué me costó -->
2026-09-23 — Setup del entorno (lección 00), Foundry configurado y prueba de humo OK con gpt-5-mini — distinguir endpoint Azure OpenAI (openai.azure.com) del de Foundry Models (services.ai.azure.com/models)
2026-09-24 — Lección 18 (fuera de orden): fine-tuning gpt-4.1-nano developerTier, deploy ckpt-step-80 en Developer Tier — valores de trainingType de la API, esperar archivos processed, leer train vs valid loss
2026-09-24 — Lección 09 (fuera de orden): generación de imágenes con gpt-image-2.5-flare y revisión del manejo de errores — elegir modelo sin acceso restringido, separar variables de deployment
2026-09-28 — Lección 01 retomada desde cero: 4 bloques teóricos y assignment en inglés (startup de turnos por WhatsApp) — prefill vs decode y cuello de botella; alucinación por frecuencia en datos, no por vocabulario; inglés escrito (plurales, -s de 3ª persona, sujeto/objeto)
2026-09-29 — Lección 02: clasificación de modelos, evaluación con datos propios y cuándo usar few-shot, RAG o fine-tuning — hacer la cuenta completa de costos (few-shot variable vs hosting fijo por hora); RAG no modifica el modelo ni es más robusto que el prompt
2026-10-02 — Lección 03: IA responsable aplicada a mi asistente de turnos (transparencia, sesgos, estafa, jailbreak, incidentes) + challenge de Content Safety — defensa probabilística (filtros, prompt) vs determinista (permisos en el backend); no culpar a la IA sin revisar logs; la frontera de la IA responsable es el daño
