# Ejercicio 1 — Comparar Greedy y A* en el mapa de Rumania

## Contexto

En el proyecto `Búsqueda informada/project` (AIMA cap. 3–4, Figuras 3.2 y 3.22)
se resuelve el problema de **encontrar una ruta** entre dos ciudades del mapa
carretero de Rumania. Dos algoritmos de búsqueda **informada** comparten el
mismo grafo, el mismo `RouteFindingProblem` y la misma heurística `h(n)`:

| Programa | Algoritmo | Qué optimiza (o no) |
|---|---|---|
| `03_greedy_best_first_search.py` | Greedy best-first | Expande el menor `h(n)` (sin garantía de optimalidad) |
| `04_a_star_search.py` | A* | Expande el menor `f(n) = g(n) + h(n)` (óptimo si `h` es admisible) |

El caso por defecto es **Arad → Bucharest**. En este ejercicio **no vas a
programar** los algoritmos: vas a **elegir otra pareja origen–destino**,
ejecutar ambos métodos y **explicar** por qué coinciden o discrepan.

Los vecinos se expanden en **orden alfabético**, así que los resultados son
deterministas si usas la misma pareja de ciudades.

A* (y Greedy) necesitan `h(n)` = estimado desde **cualquier ciudad** hasta el
destino que elegiste. Eso ya está resuelto: no implementas `h`. Al pasar
`--to DESTINO`, `heuristic_for` construye `h(ciudad)` para las 20 ciudades:

- Si el destino es **Bucharest**, usa la **distancia en línea recta** de la
  tabla AIMA (admisible y consistente).
- Si el destino es **cualquier otra ciudad**, usa la **distancia euclidiana**
  entre las coordenadas del mapa (también admisible: nunca sobreestima el
  costo por carretera).

Puedes verificarlo con `python 02_heuristics.py --to DESTINO`: imprime `h`
de cada ciudad hacia ese destino.

## Objetivo

Elegir una ruta distinta de Arad → Bucharest, inspeccionar `h(n)`, correr
Greedy y A*, y analizar diferencias de camino, costo, profundidad y nodos
expandidos a la luz de `g`, `h` y `f`.

## Archivos a crear / modificar

No modifiques el código de `romania/` ni de `search/`.

Trabaja solo con los scripts `01`–`04` y los flags `--from-city` y `--to`.

## Requisitos de la instancia

1. Elige un origen y un destino **distintos** de la pareja por defecto
   (`Arad`, `Bucharest`). Ambos deben existir en el mapa (ver
   `01_romania_map.py` o `romania/map.py`).
2. Debe existir **al menos un camino** entre ellos (el grafo no está
   completamente conectado: por ejemplo, Neamt solo llega vía Iasi).
3. Usa la **misma** pareja origen–destino en Greedy y en A*.
4. El destino puede ser **cualquier ciudad** del mapa (no hace falta que sea
   Bucharest): `h(n)` se calcula sola hacia ese destino.

### Parejas sugeridas (elige una o inventa la tuya)

- `Timisoara` → `Bucharest`
- `Oradea` → `Bucharest`
- `Lugoj` → `Hirsova`
- `Zerind` → `Craiova`
- `Oradea` → `Eforie`

## Pasos sugeridos

1. Activa el entorno e instala dependencias si aún no lo has hecho:

```bash
cd "Búsqueda informada/project"
python3 -m venv venv
source venv/bin/activate          # Windows: .\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

2. Explora el mapa y confirma que tus ciudades existen:

```bash
python 01_romania_map.py
python 01_romania_map.py --from-city Timisoara
```

3. Imprime `h(n)` hacia **tu destino** (no copies la tabla de Bucharest si tu
   `--to` es otra ciudad):

```bash
python 02_heuristics.py --from-city ORIGEN --to DESTINO
```

Anota los valores de `h` de las ciudades vecinas al origen: Greedy va a
preferir la que se vea “más cerca” del destino, aunque el tramo sea caro.

4. Ejecuta ambos algoritmos con tu pareja (sustituye origen y destino):

```bash
python 03_greedy_best_first_search.py --from-city ORIGEN --to DESTINO
python 04_a_star_search.py           --from-city ORIGEN --to DESTINO
```

5. Anota para cada corrida: **Status**, **Path**, **Depth** (roads), **Cost**
   (km), **Expanded**, **Generated** y la tabla de **g / h / f** a lo largo del
   camino.

6. Dibuja (papel o ASCII) el subgrafo relevante: las ciudades que aparecen en
   los caminos que obtuviste y las aristas entre ellas, con sus km. Marca
   también `h(n)` de cada ciudad.

## Criterios de aceptación

- La pareja origen–destino **no** es Arad → Bucharest.
- Corriste Greedy y A* sobre esa misma pareja.
- Consultaste `02_heuristics.py` para el mismo destino.
- En tu reporte queda claro:
  - si Greedy y A* devolvieron el **mismo** camino o no, y por qué;
  - qué heurística se usó (tabla AIMA vs. euclidiana);
  - en al menos un punto de decisión, cómo `h(n)` (Greedy) frente a
    `f(n) = g(n) + h(n)` (A*) explica la ciudad que cada algoritmo expandió.
- Incluyes evidencias (capturas o salida de terminal) de las corridas.

## Entrega

1. La pareja origen–destino elegida y un diagrama del subgrafo usado (con km
   y, si cabe, `h` de cada ciudad).
2. Una tabla comparativa con Path, Depth, Cost, Expanded (y la heurística
   usada).
3. Un breve reporte (media página) que responda:
   - ¿A* encontró el camino de **menos km**? ¿Greedy coincidió o se desvió?
   - ¿Por qué Greedy puede devolver un camino más caro aunque `h` sea
     admisible?
   - En el camino de A*, ¿`f` tiende a **no disminuir** a lo largo de la ruta?
     Relaciónalo con que `h` sea consistente (en particular si el destino es
     Bucharest y se usa la tabla AIMA).
4. Evidencias de haber ejecutado Greedy, A* y el listado de heurísticas.

## Reto opcional

- Elige una pareja en la que Greedy y A* **discrepen** claramente (Greedy
  “se acerca” en línea recta pero paga más km). Compara además el número de
  nodos expandidos: ¿cuál algoritmo “trabajó” más en tu instancia?
- Corre la **misma** pareja con UCS en
  `Búsqueda no informada/project` (`03_uniform_cost_search.py`). Si `h` es
  admisible, el costo de A* debería coincidir con el de UCS; Greedy no
  tiene por qué.
- Cambia solo el destino (mismo origen): una vez a Bucharest y otra a una
  ciudad distinta. Observa cómo cambia la etiqueta de la heurística y si
  Greedy sigue (o deja de) coincidir con A*.

## Pistas

- Greedy ordena la frontera solo por **`h(n)`** y **ignora** el costo
  acumulado `g(n)`. A* usa **`f(n) = g(n) + h(n)`**.
- Una heurística **admisible** nunca sobreestima el costo real al destino;
  entonces A* (esta versión de grafo, con `h` también **consistente**)
  devuelve el camino óptimo en km.
- En Arad → Bucharest (solo como referencia, no la uses de entrega), Greedy
  elige Fagaras (`h = 176`) sobre Rimnicu Vilcea (`h = 193`) y termina en
  450 km; A* paga el desvío por Rimnicu Vilcea y Pitesti y obtiene 418 km.
- Si DLS/BFS del ejercicio de búsqueda no informada ya te dieron un camino
  corto en **carreteras**, no asumas que es el de menos **km**: aquí importa
  el costo, guiado por `h`.
- Los nombres de ciudad deben coincidir **exactamente** (p. ej.
  `Rimnicu Vilcea`, no `Rimnicu`).

## Solución

### 1. Pareja origen–destino, heurística y subgrafo

Se elige **Oradea → Eforie**. Como el destino no es Bucharest, entonces `heuristic_for` usa distancia euclidiana a Eforie:

`python3 02_heuristics.py --to Eforie`
```
Heuristic: Euclidean distance to Eforie (map coordinates)
      0  Eforie  <- goal
     64  Hirsova
    120  Urziceni
    166  Bucharest
    253  Pitesti
    301  Fagaras
    349  Rimnicu Vilcea
    391  Sibiu
    513  Oradea  <- start
```

El subgrafo queda de la siguiente manera: (Greedy arriba y A* abajo)

```
                              - (99km) -> Fagaras (h=301) (211km) --------------------------------|
                              |                                                                   |
Oradea (h=513) (151km) -> Sibiu(h=391)                                                            -> Bucharest (h=166) -> Urziceni (h=120) (98km) -> Hirsova (h=64) (86km) -> Eforie (h=0)
                              |                                                                   |
                              - (80km) -> Rimnicu Vilcea(h=349) (97km) -> Pitesti (h=253) (101km) -


```


### 2. Tabla comparativa

| Algoritmo | Status  | Path (resumen)                                                        | Depth | Cost (km) | Expanded  | Generated |
|-----------|---------|-----------------------------------------------------------------------|-------|-----------|-----------|-----------|
| Greedy    | success | Oradea→Sibiu→Fagaras→Bucharest→Urziceni→Hirsova→Eforie                | 6     | 730       | 6         | 18        |
| A*        | success | Oradea→Sibiu→Rimnicu Vilcea→Pitesti→Bucharest→Urziceni→Hirsova→Eforie | 7     | 698       | 11        | 32        |

Heurística usada por ambos: Distancia euclidiana.

`python3 03_greedy_best_first_search.py --from-city Oradea --to Eforie`
```
Status:    success
Path:      Oradea → Sibiu → Fagaras → Bucharest → Urziceni → Hirsova → Eforie
Depth:     6 roads   Cost: 730 km

  city              g     h     f
  Oradea            0   513   513
  Sibiu           151   391   542
  Fagaras         250   301   551
  Bucharest       461   166   627
  Urziceni        546   120   666
  Hirsova         644    64   708
  Eforie          730     0   730

Expanded: 6   Generated: 18
```
`python3 04_a_star_search.py --from-city Oradea --to Eforie`
```
Status:    success
Path:      Oradea → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest → Urziceni → Hirsova → Eforie
Depth:     7 roads   Cost: 698 km

  city              g     h     f
  Oradea            0   513   513
  Sibiu           151   391   542
  Rimnicu Vilcea  231   349   580
  Pitesti         328   253   581
  Bucharest       429   166   595
  Urziceni        514   120   634
  Hirsova         612    64   676
  Eforie          698     0   698

Expanded: 11   Generated: 32
```

### 3. Reporte de resultados

**¿A* encontró el camino de menos km? ¿Greedy coincidió o se desvió?**
Para A* sí, con 698 km. Por otro lado, Greedy se desvía y paga 730 km a cambio de una carretera menos.
En Sibiu, Greedy elige Fagaras sobre Rimnicu Vilcea por tener menos hops, ignorando que el tramo por Fagaras hasta Bucharest es más caro en kilómetros.

**¿Por qué Greedy puede devolver un camino más caro aunque h sea admisible?**
Greedy ordena la frontera solo por h e ignora el costo acumulado (g): se mueve según su cercanía en línea recta (distancia euclidiana) sin medir cuánto cuesta
llegar ahí. Que h sea admisible solo garantiza que no siempre quiera escoger el primer camino.

**¿f no decrece en el camino de A*?**
Según los logs de A*, f va: 513, 542, 580, 581, 595, 634, 676, 698. Es decir, no decrece.
Esto se debe a que cumple la desigualdad del triángulo, por lo que f nunca puede bajar de un nodo a su hijo; por eso A*
se expande en orden de f (creciente) y el primer Eforie que saca de la frontera ya está el optimizado.