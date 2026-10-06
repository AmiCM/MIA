# Reporte — RAG de perfumería

**Dominio y corpus.** Catálogo de perfumes [FragDB](https://github.com/FragDB/fragrance-database) (CC-BY-NC-4.0; datos de [Fragrantica](https://www.fragrantica.com)), muestras gratuitas: 33 documentos
Markdown (10 perfumes, notas, marcas, perfumistas, 20 noticias), ~29 000 palabras, **152 chunks**.
Embeddings: `gemini-embedding-001`; generación: `gemini-3.8-flash`. Documentos en inglés, preguntas en español.

**Chunking.** 250 palabras con 50 de solape (20 %). Un perfume ocupa ~1–2 chunks, así que cada chunk
conserva ficha técnica y descripción juntas; el solape evita cortar una idea en el borde.

**Abstención.** Dos filtros: (1) si el mejor chunk tiene similitud coseno < `MIN_SCORE` = 0.63 no se llama
a Gemini; (2) Gemini debe responder `NO_EVIDENCIA` si los chunks no contienen la respuesta.
El umbral se calibró con `scripts/calibrate.py` sobre 25 preguntas etiquetadas (mejor score por pregunta):

| Grupo | n | Mejor score |
|---|---|---|
| Respondibles | 15 | ≥ 0.711 |
| Imposibles ajenas al dominio (Mongolia, paella…) | 6 | 0.505 – 0.553 |
| Imposibles del dominio (Aventus, Baccarat Rouge 540…) | 4 | 0.659 – 0.689 |

0.63 es el punto medio entre ajenas y respondibles: 0 % de respondibles rechazadas y 0 % de ajenas
aceptadas. Las imposibles del dominio puntúan alto porque "suenan" a perfumería; el umbral no las separa
y las frena el filtro 2 (Gemini se abstuvo en las 4). Subir a 0.70 las frenaría también, pero deja solo
0.011 de margen sobre la peor respondible, demasiado justo con tan pocas preguntas.

**Reparto de responsabilidades.** Google AI: vectores (documento/consulta, mismo modelo) y redacción de
la respuesta con citas. ChromaDB: persistencia en disco y k-NN coseno sobre los vectores que le pasamos.
FastAPI: chunking, orquestación y umbral. Streamlit: solo cliente HTTP.

**Limitaciones.** Preguntas agregadas ("¿qué perfumes duran más y son nocturnos?") fallan porque top-k
solo ve 4 chunks; las muestras tienen solo 10 perfumes y pocas notas/acordes resueltos.

## Evidencias
Ver `EVIDENCIAS.md` (curl) y añadir capturas de Streamlit y `/docs`.

## Atribución
Datos: **FragDB – Fragrance Database** (<https://fragdb.net>, <https://github.com/FragDB/fragrance-database>, v5.17), licencia CC-BY-NC-4.0,
con contenido original de Fragrantica. Uso exclusivamente académico y no comercial. Cambios: conversión a Markdown,
limpieza de HTML, resolución de ids a nombres y resumen de votos (`scripts/build_corpus.py`).
