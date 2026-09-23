---
name: cerrar-tema
description: Cierra un tema, ejercicio o lección y propone el commit del progreso. Úsalo cuando el usuario diga que terminó algo, que quiere guardar el progreso o que va a cortar la sesión.
---

# Cerrar tema y proponer commit

1. **Repaso:** hazme 2–3 preguntas cortas sobre lo visto. Si fallo alguna, repasa ese punto antes de seguir.
2. **Notas:** actualiza `aprendizaje/leccion-XX/notas.md` (conceptos, qué hice, dudas pendientes, resumen en una frase).
3. **Progreso:** actualiza `aprendizaje/PROGRESO.md`:
   - Estado de la lección (🟡 En curso o ✅ Terminada, con fecha de fin).
   - Una línea en "Bitácora": fecha — qué hice — qué me costó.
4. **Seguridad antes del commit:**
   - Confirma que `.env` no aparece en `git status`.
   - Busca en los archivos a commitear posibles secretos (`key`, `token`, `credential`, `secret`). Si encuentras algo, avísame y no lo incluyas.
   - Si hay notebooks con salidas, pídeme que las limpie (VS Code: "Clear All Outputs") o que confirme que no contienen datos sensibles.
   - Confirma que no se modificaron archivos del curso original. Si hay, avísame antes de continuar.
5. **Propuesta:** muéstrame:
   - La salida de `git status`.
   - Los archivos a incluir, con `git add` y rutas explícitas (nunca `git add .`).
   - El mensaje de commit con el formato de `CLAUDE.md`.
6. **Espera mi confirmación explícita.**
   - Si digo que sí: ejecuta `git add` y `git commit`.
   - Si pido cambios: ajusta y vuelve a proponer.
7. No hagas `git push` salvo que te lo pida.
