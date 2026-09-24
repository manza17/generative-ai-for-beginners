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
4. **Progreso:** actualiza `aprendizaje/PROGRESO.md`:
   - Estado de la lección (🟡 En curso o ✅ Terminada, con fecha de fin).
   - Una línea en "Bitácora": fecha — qué hice — qué me costó.
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
