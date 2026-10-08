---
name: cerrar-tema
description: Cierra un tema, ejercicio o lección y propone el commit del progreso. Úsalo cuando el usuario diga que terminó algo, que quiere guardar el progreso o que va a cortar la sesión.
---

# Cerrar tema y proponer commit

1. **Repaso:** hazme 2–3 preguntas cortas sobre lo visto. Si fallo alguna, repasa ese punto antes de seguir.
2. **Notas:** revisa `aprendizaje/leccion-XX/notas.md` (conceptos, qué hice, dudas pendientes, resumen en una frase). Respeta mis palabras: agrega correcciones conceptuales y mejoras de redacción marcadas con ✏️.
3. **Repaso escrito:** crea o actualiza `aprendizaje/leccion-XX/repaso.md` como material de repaso:
   - Qué hicimos, en orden (incluidas decisiones y pasos del portal).
   - El código bloque por bloque, con las explicaciones que diste en la sesión.
   - Gotchas y errores que aparecieron, con su causa.
   - 4–5 preguntas de autoevaluación.
   - **Resumen AI-103:** si en la lección apareció algo relevante para la certificación Microsoft AI-103 (código o conceptos de Azure: clientes, APIs, parámetros, servicios), crea `aprendizaje/leccion-XX/ai-103.md`: solo lo de Azure, con código mínimo, diferencias que suelen preguntar y trampas típicas. Agrega una línea por lección en el índice `aprendizaje/AI-103.md`. Si la lección no tiene nada de Azure, omite este paso.
4. **Progreso:** actualiza `aprendizaje/PROGRESO.md`:
   - Estado de la lección (🟡 En curso o ✅ Terminada, con fecha de fin).
   - Una línea en "Bitácora": fecha — qué hice — qué me costó.
   - **Tablero de Notion:** si la lección quedó ✅, márcala en la página `ruta-ia-agentica-tasklist` (id `3c73dda0e9ce82c3b3700141dd0e2e97`), sección "Fase 0", cambiando `- [ ]` por `- [x]` en su ítem con `update_content` (edición mínima, nunca reemplazar la página entera). Usa esta tabla para no confundir ítems parecidos:

     | # | Ítem en Notion | # | Ítem en Notion |
     |---|---|---|---|
     | 00 | Configuración del curso (Course Setup) | 11 | Function calling |
     | 01 | Introducción a la IA generativa y los LLMs | 12 | UX para apps de IA |
     | 02 | Explorar y comparar distintos LLMs | 13 | Seguridad en apps de IA generativa |
     | 03 | Uso responsable de la IA generativa | 14 | Ciclo de vida de apps de IA generativa (LLMOps) |
     | 04 | Fundamentos de prompt engineering | 15 | RAG y bases de datos vectoriales |
     | 05 | Prompts avanzados | 16 | Modelos open source |
     | 06 | Apps de generación de texto | 17 | Agentes de IA |
     | 07 | Apps de chat | 18 | Fine-tuning |
     | 08 | Apps de búsqueda | 19 | Small Language Models (SLMs) |
     | 09 | Crear app generación de imagen. | 20 | Modelos de Mistral |
     | 10 | Apps low code | 21 | Modelos de Meta |

     - Antes de editar, haz `fetch` de la página para confirmar el texto exacto del ítem.
     - Si el ítem no existe, agrégalo en su posición según el orden del curso, ya marcado.
     - Si el conector de Notion no está disponible, avísame y sigue con el resto del cierre.
     - Notion no forma parte del commit: es un cambio externo, avísame cuando lo hagas.
5. **Seguridad antes del commit:**
   - Confirma que `.env` no aparece en `git status`.
   - Busca en los archivos a commitear posibles secretos (`key`, `token`, `credential`, `secret`). Si encuentras algo, avísame y no lo incluyas.
   - Si hay notebooks con salidas, pídeme que las limpie (VS Code: "Clear All Outputs") o que confirme que no contienen datos sensibles.
   - Confirma que no se modificaron archivos del curso original. Si hay, avísame antes de continuar.
6. **Propuesta:** muéstrame:
   - La salida de `git status`.
   - Los archivos a incluir, con `git add` y rutas explícitas (nunca `git add .`).
   - El mensaje de commit con el formato de `CLAUDE.md`.
7. **Espera mi confirmación explícita.**
   - Si digo que sí: ejecuta `git add` y `git commit`.
   - Si pido cambios: ajusta y vuelve a proponer.
8. No hagas `git push` salvo que te lo pida.
