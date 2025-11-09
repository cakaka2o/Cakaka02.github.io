Emojíaco — Paquete final con separadores '/'

Cambios principales:
- '/' se interpreta como separador de palabras y '//' como salto de línea, tanto en la UI como en CLI.
- Puedes activar la opción en la UI o usar el flag --slashes en mapeo.py
- Mantiene soporte para mayúsculas (marcador '👀') y para incluir/excluir la Ñ.

Archivos incluidos:
- index.html, style.css, mapping.json, mapeo.py, mapeo_check.js, mapeo_check2.json, translator.py, README.md, example files.

Ejemplos CLI:
  python mapeo.py to-emoji "Hola mundo" --slashes
  python mapeo.py to-text "😈... // 😐..." --slashes
