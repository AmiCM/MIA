# Evidencias (curl contra FastAPI)

```bash
curl -X POST localhost:8000/query -H 'content-type: application/json' \
  -d '{"question":"¿Quién creó Angel de Mugler y qué notas de base tiene?"}'
```
Respuesta: *Angel fue creado por Olivier Cresp e Yves de Chiris [1]… base: pachulí, vainilla, ámbar, almizcle, sándalo [1]*. Top score 0.757 (`704-angel.md`).

**Fuera de dominio** — "¿Cuál es la capital de Mongolia?" → `abstained: true`, "No tengo evidencia suficiente…" (mejor score 0.505).

## Capturas (carpeta `evidencias/`)
1. `01_docs_endpoints.png` — `/docs` con los endpoints.
2. `02_docs_query_con_citas.png` — `POST /query` en Swagger, respuesta con citas y scores.
3. `03_docs_query_abstencion.png` — misma API, pregunta fuera de dominio (`abstained: true`).
4. `04_streamlit_respuesta_con_citas.png` — Streamlit: respuesta con `[n]`, chunks y scores.
5. `05_streamlit_abstencion.png` — Streamlit: abstención.
