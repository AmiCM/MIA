# Attribution

El corpus de `data/` se deriva de las **muestras gratuitas de FragDB**, licenciadas bajo
[CC-BY-NC-4.0](https://creativecommons.org/licenses/by-nc/4.0/) (solo uso no comercial; este proyecto es académico).

- Dataset: **FragDB – Fragrance Database** · repositorio <https://github.com/FragDB/fragrance-database> · sitio <https://fragdb.net> · versión v5.17 (2026-09-30).
- El contenido de perfumes, notas, marcas, perfumistas, reseñas y noticias proviene de **Fragrantica** (<https://www.fragrantica.com>), recopilado por FragDB.
- **Cambios realizados:** se convirtieron los CSV/parquet en documentos Markdown (`scripts/build_corpus.py`): se limpió el HTML, se resolvieron ids de notas/acordes a nombres, se resumieron votos de la comunidad y se unieron reseñas al documento de cada perfume. Los datos no se alteraron en su contenido.
- El dataset completo es de pago y no se redistribuye aquí; para regenerar el corpus con él, adquiérelo en fragdb.net.
