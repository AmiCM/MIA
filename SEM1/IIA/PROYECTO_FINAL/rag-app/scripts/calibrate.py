"""Calibra MIN_SCORE: mide el score del mejor chunk en preguntas respondibles vs. imposibles.

Requiere la API en marcha e índice cargado. No llama a Gemini (usa retrieve_only).
  python scripts/calibrate.py [--api http://localhost:8000] [--set scripts/calibration_set.json]
"""
import argparse
import json
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent


def best_score(api: str, q: str) -> float:
    r = httpx.post(f"{api}/query", json={"question": q, "top_k": 1, "retrieve_only": True}, timeout=60)
    r.raise_for_status()
    hits = r.json()["citations"]
    return hits[0]["score"] if hits else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--api", default="http://localhost:8000")
    ap.add_argument("--set", default=str(ROOT / "calibration_set.json"))
    a = ap.parse_args()
    data = json.loads(Path(a.set).read_text(encoding="utf-8"))

    scores = {g: [(q, best_score(a.api, q)) for q in qs] for g, qs in data.items()}
    for g, rows in scores.items():
        print(f"\n== {g} ==")
        for q, s in sorted(rows, key=lambda x: x[1]):
            print(f"  {s:.3f}  {q}")
        vals = [s for _, s in rows]
        print(f"  min={min(vals):.3f}  media={sum(vals)/len(vals):.3f}  max={max(vals):.3f}")

    ans = [s for _, s in scores["answerable"]]
    unrel = [s for _, s in scores.get("impossible_unrelated", [])]
    indom = [s for _, s in scores.get("impossible_in_domain", [])]

    print("\n== Barrido de umbrales ==")
    print("umbral | rechaza respondibles | deja pasar ajenas | deja pasar del dominio")
    for t in [x / 100 for x in range(40, 85, 5)]:
        fr = sum(s < t for s in ans) / len(ans)
        fa_u = sum(s >= t for s in unrel) / len(unrel) if unrel else 0
        fa_d = sum(s >= t for s in indom) / len(indom) if indom else 0
        print(f"{t:6.2f} | {fr:20.0%} | {fa_u:17.0%} | {fa_d:22.0%}")

    lo, hi = max(unrel, default=0), min(ans)
    print(f"\nMejor score en preguntas ajenas: {lo:.3f}; peor en respondibles: {hi:.3f}")
    if lo < hi:
        print(f"Umbral recomendado (punto medio): {(lo + hi) / 2:.2f}")
    else:
        print("Las distribuciones se solapan: ningún umbral separa limpiamente; prioriza no rechazar respondibles.")
    print("Nota: las preguntas imposibles del dominio suelen puntuar alto; las filtra Gemini (NO_EVIDENCIA), no el umbral.")


if __name__ == "__main__":
    main()
