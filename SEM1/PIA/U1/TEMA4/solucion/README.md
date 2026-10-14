# Catálogo de cursos con MCP · Solución

Una función consulta `data/courses.json`. `main.py` la usa desde la terminal y
`server.py` la expone como herramienta MCP mediante stdio.

| Cambio                                                    | Archivo                   |
|---|---|
| Catálogo ampliado con un tercer curso de Python (`PY03`)  | `data/extra_courses.json` |
| Mensaje INFO con total de cursos leídos y coincidencias   | `catalog/search.py`       |
| Respuestas y evidencia de los ejercicios 1–7              | `README.md`               |

Ejecuta:
```bash
uv sync --locked
uv run --locked python main.py python
uv run --locked python main.py python --catalog data/extra_courses.json
uv run --locked python client.py python
make check
```

NOTA: Las rutas absolutas de los tracebacks se abreviaron como `…/`.

---

## Ejercicio 1 · Punto de entrada

```console
$ uv run python -c "import main"
[exit code: 0]

$ uv run python -c "
import asyncio, server
tools = asyncio.run(server.mcp.list_tools())
print('Imported server; registered tools:', [t.name for t in tools])
print('__name__ of the module:', server.__name__)
"
Imported server; registered tools: ['find_courses']
__name__ of the module: server
[exit code: 0]
```

**¿Por qué `import main` no consulta el catálogo?** Importar un módulo ejecuta su código
de nivel superior, es decir lo que se encuentra en el archivo base ejecutado, todo lo que no esté bajo el archivo base ejecutado y que esté bajo el
`if __name__ == "__main__":` No será ejecutado hasta que sea explícitamente llamado o será mostrado en caso de error para el Traceback.

**¿Qué impide iniciar el transporte al importar `server.py`?** La misma condición __name__=='__main__' antes señalada:

```python
if __name__ == "__main__":
    configure_logging()
    mcp.run(transport="stdio")
```

**Registrar frente a iniciar.** Al importar `server` se ejecutan
`mcp = MCPServer(...)` y el decorador `@mcp.tool()`. Al "registrar" la herramienta, esta añade
`find_courses` a la tabla de herramientas del servidor, con su descripción generada a
partir de las anotaciones y del docstring, de ahí que `list_tools()` la muestra sin que
haya un servidor en marcha. **Iniciar** el servidor (`mcp.run`) abre el transporte stdio
y queda bloqueado esperando mensajes MCP por stdin.

---

## Ejercicio 2 · Datos y argumentos

`data/extra_courses.json` es una copia de `data/courses.json` con un curso más:

```json
{ "code": "PY03", "title": "Python for machine learning", "hours": 18 }
```

```console
$ uv run python main.py python --catalog data/extra_courses.json
INFO | catalog.search | Search completed: 3 matches out of 4 courses read
[
  {
    "code": "PY01",
    "title": "Python foundations",
    "hours": 12
  },
  {
    "code": "PY02",
    "title": "Python for data analysis",
    "hours": 16
  },
  {
    "code": "PY03",
    "title": "Python for machine learning",
    "hours": 18
  }
]
[exit code: 0]

$ uv run python main.py python --catalog data/missing.json
ERROR | __main__ | Catalog search failed
Traceback (most recent call last):
  File "…/solucion/main.py", line 23, in main
    courses = search_courses(args.query, args.catalog)
  File "…/solucion/catalog/search.py", line 25, in search_courses
    with path.open(encoding="utf-8") as source:
         ~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "…/python3.13/pathlib/_local.py", line 537, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'data/missing.json'
[exit code: 1]
```

- Con `--catalog data/extra_courses.json` aparecen tres resultados (PY01, PY02 y
  PY03). `ML01` no coincide porque su título no contiene «python».
- Con una ruta inexistente, `search_courses` lanza `FileNotFoundError` (subclase de
  `OSError`). `main.py` la captura, la registra con traceback mediante
  `logger.exception` y devuelve código de salida 1 o Exit code 1 (Error de ejecución). Como un archivo ausente es un error,
  no una búsqueda sin coincidencias.
- La herramienta MCP no acepta `--catalog`: `find_courses` llama a
  `search_courses(query)` con `DEFAULT_CATALOG`. Por eso `client.py python` sigue
  devolviendo dos cursos.

---

## Ejercicio 3 · Niveles y destinos

La salida JSON se envía a `/dev/null` para ver sólo los logs (stderr).

```console
$ uv run python main.py python --log-level DEBUG > /dev/null
DEBUG | catalog.search | Reading catalog: …/solucion/data/courses.json
INFO | catalog.search | Search completed: 2 matches out of 3 courses read
[exit code: 0]

$ uv run python main.py python --log-level INFO > /dev/null
INFO | catalog.search | Search completed: 2 matches out of 3 courses read
[exit code: 0]

$ uv run python main.py python --log-level ERROR > /dev/null
[exit code: 0]

$ uv run python main.py python --log-level ERROR --log-file logs/app.log > /dev/null
[exit code: 0]

$ cat logs/app.log
DEBUG | catalog.search | Reading catalog: …/solucion/data/courses.json
INFO | catalog.search | Search completed: 2 matches out of 3 courses read
[exit code: 0]

$ uv run python main.py python > result.json && head -3 result.json
INFO | catalog.search | Search completed: 2 matches out of 3 courses read
[
  {
    "code": "PY01",
[exit code: 0]
```

**Comparación de niveles.** DEBUG muestra la ruta leída y el resumen mientras que INFO sólo el
resumen y ERROR no muestra nada porque la consulta no falló. El nivel filtra mensajes
por severidad.

**¿Por qué el archivo conserva mensajes que no aparecen en consola?** En
`configure_logging`, el logger raíz acepta desde DEBUG y cada handler aplica su propio
filtro. El handler de consola usa el nivel pedido (`ERROR`) y descarta DEBUG e INFO.
Como el `FileHandler` está fijado en DEBUG entonces los guarda todos. Los mensajes son los mismos;
cada destino decide cuáles conserva.

**¿Por qué stdout se reserva al protocolo en `server.py`?** Con transporte stdio, el
cliente y el servidor intercambian mensajes JSON-RPC por stdin/stdout. Cualquier texto
ajeno escrito en stdout (un `print`, un log) se mezclaría con esos mensajes y el cliente
no podría interpretarlos, lo que rompería la conexión. Por eso los logs van a stderr
(`StreamHandler` usa stderr por defecto).

---

## Ejercicio 4 · Mejorar el diagnóstico

Cambio en `catalog/search.py`, con argumentos de logging en lugar de una f-string,
para que el mensaje sólo se formatee si algún handler lo va a emitir:

```diff
-    logger.info("Search completed: %d matches", len(matches))
+    logger.info(
+        "Search completed: %d matches out of %d courses read",
+        len(matches),
+        len(courses),
+    )
```

Antes: `INFO | catalog.search | Search completed: 2 matches`
Después: `INFO | catalog.search | Search completed: 2 matches out of 3 courses read`

**Mismos cursos por consulta directa y por MCP.** `python` → PY01 y PY02 en los dos casos.
Compárese el JSON de `main.py python` (ejercicio 3) con el `structured_content` de
`client.py python` (ejercicio 5). `astronomy` → `[]` en los dos. El cambio sólo
afecta al log, no a la búsqueda.

---

## Ejercicio 5 · Reproducción y llamada MCP

Copia limpia: el proyecto copiado a otra carpeta sin `.venv`, cachés, `logs/` ni
`result.json`.

```console
$ ls -A
.gitignore
.python-version
Makefile
README.md
catalog
client.py
data
main.py
pyproject.toml
server.py
tests
uv.lock
[exit code: 0]

$ uv sync --locked
Using CPython 3.13.13
Creating virtual environment at: .venv
Resolved 43 packages in 0.68ms
Installed 39 packages in 98ms
 + annotated-types==0.8.0
 …
 + mcp==2.2.0
 …
 + pydantic==2.13.5
 …
[exit code: 0]

$ uv run --locked python client.py python
INFO | catalog.search | Search completed: 2 matches out of 3 courses read
Tools: ['find_courses']
{
  "meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "Course catalog",
      "version": ""
    }
  },
  "content": [
    {
      "type": "text",
      "text": "{\n  \"code\": \"PY01\",\n  \"title\": \"Python foundations\",\n  \"hours\": 12\n}",
      "annotations": null,
      "meta": null
    },
    {
      "type": "text",
      "text": "{\n  \"code\": \"PY02\",\n  \"title\": \"Python for data analysis\",\n  \"hours\": 16\n}",
      "annotations": null,
      "meta": null
    }
  ],
  "structured_content": {
    "result": [
      {
        "code": "PY01",
        "title": "Python foundations",
        "hours": 12
      },
      {
        "code": "PY02",
        "title": "Python for data analysis",
        "hours": 16
      }
    ]
  },
  "is_error": false,
  "result_type": "complete"
}
[exit code: 0]

$ uv run --locked python client.py astronomy
INFO | catalog.search | Search completed: 0 matches out of 3 courses read
Tools: ['find_courses']
{
  "meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "Course catalog",
      "version": ""
    }
  },
  "content": [],
  "structured_content": {
    "result": []
  },
  "is_error": false,
  "result_type": "complete"
}
[exit code: 0]

$ uv run --locked python client.py "   "
ERROR | __main__ | Catalog search failed
Traceback (most recent call last):
  File "…/course-catalog/server.py", line 19, in find_courses
    return search_courses(query)
  File "…/course-catalog/catalog/search.py", line 23, in search_courses
    raise ValueError("Query must not be blank")
ValueError: Query must not be blank
INFO | mcp.server.mcpserver.server | Tool 'find_courses' failed: 'Error executing tool find_courses: Cannot search the catalog. Check the query and server logs.'
Tools: ['find_courses']
{
  "meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "Course catalog",
      "version": ""
    }
  },
  "content": [
    {
      "type": "text",
      "text": "Error executing tool find_courses: Cannot search the catalog. Check the query and server logs.",
      "annotations": null,
      "meta": null
    }
  ],
  "structured_content": null,
  "is_error": true,
  "result_type": "complete"
}
[exit code: 1]
```

**Herramienta disponible:** `Tools: ['find_courses']`. El cliente la descubre con
`list_tools()` antes de llamarla.

**Respuesta vacía frente a error.**

| Consulta | `is_error` | Contenido | Código de salida | Significado |
|---|---|---|---|---|
| `python` | `false` | `result` con PY01 y PY02 | 0 | Búsqueda correcta con coincidencias. |
| `astronomy` | `false` | `result: []` | 0 | Búsqueda correcta **sin** coincidencias: una respuesta válida. |
| `"   "` | `true` | mensaje de error, sin `structured_content` | 1 | La búsqueda **no pudo hacerse**: consulta en blanco. |

La lista vacía es un resultado legítimo; el error indica que la operación falló. El
servidor registra el detalle (`ValueError` con traceback) en su stderr y al cliente sólo
le envía un `ToolError` con un mensaje genérico, sin exponer detalles internos. El
servidor sigue atendiendo peticiones después del error: `tests/test_mcp.py`.

**Qué aporta cada archivo de reproducción.**

- `pyproject.toml`: nombre del proyecto, versión de Python compatible, dependencias, configuración de Ruff y pytest. Describe
  qué necesita el proyecto para correr adecuadamente (al menos hasta donde el dev puede comprobar).
- `uv.lock`: Definición exacta de todas las dependencias, directas e indirectas con versiones y hashes. Si se necesita una librería para funcionar y alguna sub librería de la cual dependa etc.
- `.python-version`: versión de python.
- **`.venv` no se entrega** Porque uv lo maneja por nosotros (es uno de los motivos principales de usar uv).

---

## Ejercicio 6 · Corregir un aviso de Ruff

Se añadió `import os` a `catalog/search.py` para validar el checker de ruff:

```console
$ uv run --locked ruff check .
F401 [*] `os` imported but unused
 --> catalog/search.py:5:8
  |
3 | import json
4 | import logging
5 | import os
  |        ^^
6 | from pathlib import Path
  |
help: Remove unused import: `os`
  |
4 | import logging
  - import os
5 | from pathlib import Path
  |

Found 1 error.
[*] 1 fixable with the `--fix` option.
[exit code: 1]
```

**Corrección:** se eliminó la línea `import os`:

```console
$ uv run --locked ruff check .
All checks passed!
[exit code: 0]
```

Ruff marca **F401** porque un import sin usar es código muerto: añade una dependencia
aparente y suele indicar un error.

---

## Ejercicio 7 · Comprobar desde una copia limpia

Nueva copia limpia del proyecto final (sin `.venv` ni cachés), con las comprobaciones de
[CALIDAD.md](../CALIDAD.md) sobre las pruebas existentes sin pruebas ruff.

```console
$ uv sync --locked
Using CPython 3.13.13
Creating virtual environment at: .venv
Resolved 43 packages in 0.98ms
…
[exit code: 0]

$ uv run --locked ruff check .
All checks passed!
[exit code: 0]

$ uv run --locked ruff format --check .
9 files already formatted
[exit code: 0]

$ uv run --locked mypy --strict main.py server.py client.py catalog
Success: no issues found in 6 source files
[exit code: 0]

$ uv run --locked python -m pytest
......                                                                   [100%]
6 passed in 1.07s
[exit code: 0]
```

Con el Makefile:

```console
$ make check
uv run --locked ruff check .
All checks passed!
uv run --locked ruff format --check .
9 files already formatted
uv run --locked mypy --strict main.py server.py client.py catalog
Success: no issues found in 6 source files
uv run --locked python -m pytest
......                                                                   [100%]
6 passed in 0.68s
[exit code: 0]
```

---

## Demostraciones opcionales

Estas dos secciones de la [guía](../GUIA.md) no son ejercicios entregables. Se
incluyen como evidencia adicional.

### MCP Inspector (GUIA §7)


**Interfaz web** (interactiva). Abre la URL local que muestra, y llama a `find_courses`:

```bash
npx @modelcontextprotocol/inspector uv run --locked python server.py
```

**Modo CLI** El servidor se
describe con un archivo de configuración con el mismo formato que usan los hosts MCP. Así
se prueba también el comando:
`uv --directory /ruta/absoluta run --locked python server.py`. Para evitar que el
Inspector interprete `--locked` como opción propia, uv se pasa en `args`:

```json
{
  "mcpServers": {
    "course-catalog": {
      "command": "uv",
      "args": ["--directory", "/ruta/absoluta/solucion", "run", "--locked", "python", "server.py"]
    }
  }
}
```

`MCP_INSPECTOR_SECRET_STORE=memory` evita que Inspector intente usar el llavero del
sistema, que no está disponible en WSL. Los logs del servidor (stderr) se omiten con
`2>/dev/null`.

```console
$ export MCP_INSPECTOR_SECRET_STORE=memory
$ npx -y @modelcontextprotocol/inspector --cli --config mcp.inspector.json --server course-catalog --method tools/list
{
  "tools": [
    {
      "name": "find_courses",
      "description": "Find courses by words in their title, ignoring letter case.",
      "inputSchema": {
        "type": "object",
        "properties": { "query": { "title": "Query", "type": "string" } },
        "required": ["query"],
        "title": "find_coursesArguments"
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "result": { "items": { "$ref": "#/$defs/Course" }, "title": "Result", "type": "array" }
        },
        "required": ["result"],
        "$defs": {
          "Course": {
            "properties": {
              "code": { "title": "Code", "type": "string" },
              "title": { "title": "Title", "type": "string" },
              "hours": { "exclusiveMinimum": 0, "title": "Hours", "type": "integer" }
            },
            "required": ["code", "title", "hours"],
            "title": "Course",
            "type": "object"
          }
        },
        "title": "find_coursesOutput"
      }
    }
  ]
}
[exit code: 0]

$ npx -y @modelcontextprotocol/inspector --cli --config mcp.inspector.json --server course-catalog --method tools/call --tool-name find_courses --tool-arg query=python 2>/dev/null
{
  "content": [
    { "type": "text", "text": "{\n  \"code\": \"PY01\",\n  \"title\": \"Python foundations\",\n  \"hours\": 12\n}" },
    { "type": "text", "text": "{\n  \"code\": \"PY02\",\n  \"title\": \"Python for data analysis\",\n  \"hours\": 16\n}" }
  ],
  "structuredContent": {
    "result": [
      { "code": "PY01", "title": "Python foundations", "hours": 12 },
      { "code": "PY02", "title": "Python for data analysis", "hours": 16 }
    ]
  },
  "isError": false
}
[exit code: 0]

$ npx -y @modelcontextprotocol/inspector --cli --config mcp.inspector.json --server course-catalog --method tools/call --tool-name find_courses --tool-arg query=astronomy 2>/dev/null
{
  "content": [],
  "structuredContent": {
    "result": []
  },
  "isError": false
}
[exit code: 0]

$ npx -y @modelcontextprotocol/inspector --cli --config mcp.inspector.json --server course-catalog --method tools/call --tool-name find_courses --tool-arg 'query=   ' 2>/dev/null
{
  "content": [
    {
      "type": "text",
      "text": "Error executing tool find_courses: Cannot search the catalog. Check the query and server logs."
    }
  ],
  "isError": true
}
[exit code: 5]
```

- **La herramienta:** sólo `find_courses`, con un esquema de entrada y otro de salida
  generados a partir de las anotaciones (`query: str`, `list[Course]`) y el docstring. El
  esquema de salida incluye la restricción `hours > 0` del modelo `Course`.
- **Las respuestas:** dos cursos para `python`, una lista vacía sin error para
  `astronomy` e `isError: true` para la cadena de espacios. En este último caso el
  Inspector termina con un código distinto de 0.

Suponiendo uso de git: 

```console
$ git init -q -b main && git status --short --untracked-files=all
?? .gitignore
?? .python-version
?? Makefile
?? README.md
?? catalog/__init__.py
?? catalog/logging_config.py
?? catalog/search.py
?? client.py
?? data/courses.json
?? data/extra_courses.json
?? main.py
?? pyproject.toml
?? server.py
?? tests/test_catalog.py
?? tests/test_mcp.py
?? uv.lock
[exit code: 0]

$ git status --short --ignored | grep "^!!"
!! .venv/
!! catalog/__pycache__/
!! logs/
!! result.json
[exit code: 0]

$ git add . && git commit -q -m "Course catalog with MCP: reproducible project"
$ git log --oneline --stat
91dbabf Course catalog with MCP: reproducible project
 .gitignore                |   9 +
 .python-version           |   1 +
 Makefile                  |  30 ++
 README.md                 | 470 ++++++++++++++++++++++
 catalog/__init__.py       |   1 +
 catalog/logging_config.py |  24 ++
 catalog/search.py         |  39 ++
 client.py                 |  32 ++
 data/courses.json         |  17 +
 data/extra_courses.json   |  22 ++
 main.py                   |  32 ++
 pyproject.toml            |  28 ++
 server.py                 |  29 ++
 tests/test_catalog.py     |  31 ++
 tests/test_mcp.py         |  30 ++
 uv.lock                   | 989 ++++++++++++++++++++++++++++++++++++++++++++++
 16 files changed, 1784 insertions(+)

$ git clone -q ./course-catalog course-catalog-check && cd course-catalog-check && ls -A
.git
.gitignore
.python-version
Makefile
README.md
catalog
client.py
data
main.py
pyproject.toml
server.py
tests
uv.lock
[exit code: 0]

$ uv sync --locked
Using CPython 3.13.13
Creating virtual environment at: .venv
Resolved 43 packages in 0.87ms
…
[exit code: 0]

$ uv run --locked python client.py python   # (salida filtrada)
Tools: ['find_courses']
        "code": "PY01",
        "code": "PY02",
  "is_error": false,
[exit code: 0]
```

## Archivos

| Archivo | Responsabilidad |
|---|---|
| `catalog/search.py` | Modelo Course, lectura y búsqueda. |
| `catalog/logging_config.py` | Niveles, formato y destinos. |
| `main.py` | Argumentos de terminal y salida JSON. |
| `server.py` | Registro de la herramienta y transporte MCP. |
| `client.py` | Cliente de demostración que inicia el servidor. |
| `data/courses.json` | Catálogo predeterminado (3 cursos). |
| `data/extra_courses.json` | Catálogo ampliado del ejercicio 2 (4 cursos). |
| `tests/` | Casos de búsqueda y comunicación real por stdio. |

[Guía progresiva](../GUIA.md) · [Práctica](../PRACTICA.md) · [Calidad](../CALIDAD.md)
