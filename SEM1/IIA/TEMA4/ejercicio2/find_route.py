#!/usr/bin/env python3
"""Ruta de menor costo (km) entre dos ciudades de Mexico con A* adaptado de `Búsqueda informada/project/search/astar.py` 
"""

from __future__ import annotations

import argparse
import heapq
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_mexico_graph import haversine  # noqa: E402  (solo la funcion, no regenera nada)

GRAPH = Path(__file__).resolve().parent / "mexico_cities_graph.json"


def load_graph(path: Path = GRAPH):
    data = json.loads(path.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in data["nodes"]}
    adj: dict[int, list[tuple[int, float]]] = defaultdict(list)
    for e in data["edges"]:  # no dirigido: cada arista vale en ambos sentidos
        adj[e["source"]].append((e["target"], e["km"]))
        adj[e["target"]].append((e["source"], e["km"]))
    return nodes, adj


def resolve_city(nodes, query: str) -> tuple[int, str | None]:
    """'Nombre', 'Nombre, Estado', 'Nombre|Estado' o id. Devuelve (id, aviso)."""
    q = query.strip()
    if q.isdigit() and int(q) in nodes:
        return int(q), None
    name, _, state = q.replace("|", ",").partition(",")
    name, state = name.strip().lower(), state.strip().lower()
    hits = [n for n in nodes.values() if n["name"].lower() == name]
    if state:
        hits = [n for n in hits if n["state"].lower() == state]
    if not hits:
        raise SystemExit(f"Ciudad no encontrada: {query!r} (usa el nombre exacto del JSON)")
    hits.sort(key=lambda n: -n["population"])
    if len(hits) == 1:
        return hits[0]["id"], None
    opts = "; ".join(f"id {n['id']} {n['state']} (pob. {n['population']:,})" for n in hits)
    return hits[0]["id"], (
        f"AVISO: '{query}' es ambiguo ({len(hits)} ciudades). Se eligió la más poblada: "
        f"id {hits[0]['id']}, {hits[0]['state']}. Opciones: {opts}. "
        f"Desambigua con 'Nombre, Estado' o el id."
    )


def search(nodes, adj, start: int, goal: int, algo: str = "astar"):
    """A* (f=g+h), UCS (h=0) o Greedy (f=h). Devuelve (path, cost, expanded, generated)."""
    g_lat, g_lon = nodes[goal]["lat"], nodes[goal]["lon"]

    def h(s: int) -> float:
        return 0.0 if algo == "ucs" else haversine(nodes[s]["lat"], nodes[s]["lon"], g_lat, g_lon)

    def f(g: float, s: int) -> float:
        return h(s) if algo == "greedy" else g + h(s)

    frontier = [(f(0.0, start), 0, start)]
    parent: dict[int, int | None] = {start: None}
    best_g = {start: 0.0}
    explored: set[int] = set()
    counter = expanded = 0
    generated = 1
    while frontier:
        _f, _i, s = heapq.heappop(frontier)
        if s in explored:
            continue
        if s == goal:
            path = [s]
            while parent[path[-1]] is not None:
                path.append(parent[path[-1]])
            return path[::-1], best_g[s], expanded, generated
        explored.add(s)
        expanded += 1
        for t, km in adj[s]:
            generated += 1
            g = best_g[s] + km
            if t in explored:
                continue
            if t not in best_g or g < best_g[t]:
                best_g[t] = g
                parent[t] = s
                counter += 1
                heapq.heappush(frontier, (f(g, t), counter, t))
    return None, None, expanded, generated


def label(n) -> str:
    return f"{n['name']} ({n['state']})"


def main() -> None:
    ap = argparse.ArgumentParser(description="Ruta entre ciudades de Mexico con A*.")
    ap.add_argument("--from-city", required=True)
    ap.add_argument("--to", required=True)
    ap.add_argument("--algo", choices=["astar", "ucs", "greedy"], default="astar")
    ap.add_argument("--full", action="store_true", help="imprime todo el camino")
    args = ap.parse_args()

    nodes, adj = load_graph()
    s, warn_s = resolve_city(nodes, args.from_city)
    t, warn_t = resolve_city(nodes, args.to)
    for w in (warn_s, warn_t):
        if w:
            print(w)

    path, cost, expanded, generated = search(nodes, adj, s, t, args.algo)
    hname = {"astar": "Haversine to destination (km)", "ucs": "none (h = 0)",
             "greedy": "Haversine to destination (km), f = h"}[args.algo]
    print(f"Heuristic: {hname}")
    print(f"Algorithm: {args.algo}")
    print(f"From:      {label(nodes[s])}  (id {s})")
    print(f"To:        {label(nodes[t])}  (id {t})")
    if path is None:
        print("Status:    failure")
        return
    names = [nodes[i]["name"] for i in path]
    shown = names if args.full or len(names) <= 10 else names[:4] + ["..."] + names[-4:]
    print("Status:    success")
    print("Path:      " + " → ".join(shown))
    print(f"Depth:     {len(path) - 1} hops   Cost: {cost:.2f} km")
    print(f"Expanded:  {expanded}   Generated: {generated}")


if __name__ == "__main__":
    main()
