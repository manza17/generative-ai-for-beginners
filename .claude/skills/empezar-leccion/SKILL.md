---
name: empezar-leccion
description: Prepara el inicio de una lección del curso. Úsalo cuando el usuario diga que empieza una lección, por ejemplo "/empezar-leccion 04" o "empiezo la lección 6".
---

# Empezar una lección

Argumento: número de lección (ej.: `04`). Si no lo recibiste, pregúntalo.

1. Localiza la carpeta del curso que empieza con ese número (ej.: `04-prompt-engineering-fundamentals/`) y lee su `README.md`.
2. Crea `aprendizaje/leccion-XX/` si no existe, con un `notas.md` basado en `aprendizaje/plantilla-notas.md` (completa número, título y fecha).
3. Si la lección tiene código (carpetas `python/`, `typescript/` u otras con notebooks o scripts):
   - Lista los archivos y pregúntame cuáles quiero trabajar.
   - Copia solo esos a `aprendizaje/leccion-XX/python/` o `aprendizaje/leccion-XX/typescript/`.
   - Nunca modifiques los originales.
   - Si hay `package.json`, recuérdame ejecutar `npm install` en la copia.
4. Si el código usa GitHub Models o `GITHUB_TOKEN`, avísame y propón cómo adaptarlo a Microsoft Foundry.
5. Si el código lee variables de entorno, dime qué nombres espera para que yo las agregue a `.env`. No leas `.env`.
6. Dame un mapa de la lección:
   - Objetivos (3 viñetas).
   - Conceptos nuevos.
   - Conocimientos previos necesarios. Pregúntame si ya los tengo; si no, enséñalos primero.
7. En `aprendizaje/PROGRESO.md`, marca la lección como 🟡 En curso con la fecha de hoy.
8. No hagas commit en este paso.
