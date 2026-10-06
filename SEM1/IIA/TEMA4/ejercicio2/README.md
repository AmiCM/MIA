# Ejercicio 2 — A* en el mapa de México

Ruta de menor costo (km) entre dos ciudades del grafo de 1,000 ciudades. A* con h = haversine al destino, adaptado de `Búsqueda informada/project/search/astar.py`. El estado es el id del nodo.

## Archivos

- `find_route.py`: CLI (A*, y `--algo ucs|greedy` para comparar).
- `mexico_map.html`: Mapa interactivo con opción de ruta.
- `evidencias/`: Salida del CLI y capturas del mapa.

`find_route.py` importa haversine de `generate_mexico_graph.py` y lee `mexico_cities_graph.json`, por lo que debe ejecutarse desde `Mexico map/` del repo `inteligencia-artificial`.

## CLI

```bash
python3 find_route.py --from-city Tijuana --to Cancún
python3 find_route.py --from-city Puebla --to "Guadalupe, Nuevo León"
```

- `--algo astar|ucs|greedy`: algoritmo (default `astar`).
- `--full`: imprime el camino completo.
- Nombres repetidos: se desambigua con `"Nombre, Estado"` o el id. Si es ambiguo, se elige la más poblada y se avisa en la salida.

## Mapa

1. Abrir `mexico_map.html` en el navegador.
2. Escribir origen y destino en el panel 'Route' (autocompleta `Nombre, Estado`).
3. Elegir algoritmo y pulsar **Find route**: la ruta se pinta en azul (origen verde, destino rojo) y el panel muestra costo, hops y nodos expandidos. **Clear** la quita.

NOTA: No correr `generate_mexico_graph.py`, sobrescribe `mexico_map.html` y borra la UI.
