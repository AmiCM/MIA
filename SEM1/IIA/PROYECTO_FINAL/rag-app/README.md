# RAG de perfumería (Streamlit + FastAPI + ChromaDB + Google AI)

Corpus: [FragDB](https://github.com/FragDB/fragrance-database) (CC-BY-NC-4.0, uso académico). Ver [Atribución](#atribución-y-licencia-de-los-datos).

## Arquitectura
Streamlit (8501) → FastAPI (8000) → Google AI (embeddings + Gemini) y ChromaDB (persistente en `chroma/`).
Streamlit solo habla HTTP con la API.

## Puesta en marcha
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # pega tu GOOGLE_API_KEY (https://aistudio.google.com/apikey)

uvicorn app.main:app --reload --port 8000        # terminal 1
streamlit run ui/streamlit_app.py                # terminal 2
```
Docs de la API: http://localhost:8000/docs

## Corpus
`scripts/build_corpus.py` convierte FragDB en Markdown (`data/`): un documento por perfume
(notas, acordes, votos de duración/estela/temporada, descripción, pros/contras, reseñas),
más `notes.md`, `brands.md`, `perfumers.md` y un documento por noticia.
`data/` ya viene incluido; solo necesitas el dataset para **regenerarlo**. La carpeta `fragrance-database/`
no se sube a git (está en el `.gitignore`); clónala junto a `rag-app/`:
```bash
cd SEM1/IIA/PROYECTO_FINAL
git clone https://github.com/FragDB/fragrance-database.git
git -C fragrance-database checkout b856527   # v5.17, 2026-09-30 (la versión usada aquí)
```
Con las muestras gratuitas del repo (10 registros por CSV) salen **33 documentos, ~29 000 palabras**.
```bash
pip install pyarrow
python scripts/build_corpus.py                                   # muestras
python scripts/build_corpus.py --src /ruta/dataset --limit 300   # dataset completo, top-300 por votos
```
Los documentos están en inglés; las preguntas y respuestas son en español (embeddings multilingües).
En Streamlit, carga todos los `.md` de `data/` (incluidas las subcarpetas) con "Indexar".

## Preguntas de prueba
- ¿Quién creó Angel de Mugler y qué notas de base tiene?
- ¿Qué perfumes tienen buena duración y son para la noche?
- ¿Qué opina la gente de Black Opium?
- Fuera de dominio (debe abstenerse): ¿Cuál es la capital de Mongolia? / ¿Cuánto cuesta Aventus de Creed?

## Probar
```bash
curl -F "files=@data/fragrances/704-angel.md" -F "files=@data/notes.md" http://localhost:8000/ingest
curl -X POST localhost:8000/query -H 'content-type: application/json' \
  -d '{"question":"¿Qué es el overlap en el chunking?"}'
```

## Retos opcionales
- **Filtro por fuente**: `POST /query` acepta `source`; en la UI, selector "Limitar a un documento".
- **Borrar / reindexar**: `GET /sources`, `DELETE /sources/{source}`; volver a subir un archivo reemplaza sus chunks.
- **Histórico**: sección al final de la página de Streamlit (por sesión).
- **Docker Compose**: `docker compose up --build` (API en 8000, UI en 8501; requiere `.env`; el índice persiste en `./chroma`).

## Decisiones
- **Embeddings**: `gemini-embedding-001` (`RETRIEVAL_DOCUMENT` para chunks, `RETRIEVAL_QUERY` para preguntas; mismo modelo).
- **Chunking**: 250 palabras, 50 de solape (configurable en `.env`: `CHUNK_WORDS`, `CHUNK_OVERLAP`).
- **Chroma**: espacio coseno, vectores pasados explícitamente; `score = 1 - distancia`.
- **Abstención**: (1) si el mejor chunk tiene score < `MIN_SCORE` (0.63) no se llama a Gemini; (2) si Gemini responde `NO_EVIDENCIA`. Calibrado con `python scripts/calibrate.py` (25 preguntas): ajenas ≤ 0.553, respondibles ≥ 0.711 → punto medio 0.63.
- **Generación**: `gemini-3.8-flash`, solo con la evidencia numerada, citas `[n]`.

## Pendiente
- Calibrar `MIN_SCORE`, capturas de evidencia y reporte de una página.

## Atribución y licencia de los datos

El corpus de `data/` se deriva de las **muestras gratuitas de FragDB**, licenciadas bajo
[CC-BY-NC-4.0](https://creativecommons.org/licenses/by-nc/4.0/) (solo uso no comercial; este proyecto es académico).

- Dataset: **FragDB – Fragrance Database** · repositorio <https://github.com/FragDB/fragrance-database> · sitio <https://fragdb.net> · versión v5.17 (2026-09-30).
- El contenido de perfumes, notas, marcas, perfumistas, reseñas y noticias proviene de **Fragrantica** (<https://www.fragrantica.com>), recopilado por FragDB.
- **Cambios realizados:** se convirtieron los CSV/parquet en documentos Markdown (`scripts/build_corpus.py`): se limpió el HTML, se resolvieron ids de notas/acordes a nombres, se resumieron votos de la comunidad y se unieron reseñas al documento de cada perfume. Los datos no se alteraron en su contenido.
- El dataset completo es de pago y no se redistribuye aquí; para regenerar el corpus con él, adquiérelo en fragdb.net.
