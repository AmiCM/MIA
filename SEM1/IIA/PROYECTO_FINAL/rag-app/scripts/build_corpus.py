"""Convierte FragDB (CSV + parquet) en documentos Markdown para el RAG.

Uso:
  python scripts/build_corpus.py                       # usa ../fragrance-database/samples
  python scripts/build_corpus.py --src RUTA --limit 300  # dataset completo, top-300 por votos
"""
import argparse
import csv
import html
import json
import re
from pathlib import Path

csv.field_size_limit(10**9)
ROOT = Path(__file__).resolve().parent.parent


def read_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="|"))


def read_parquet(path: Path) -> list[dict]:
    if not path.exists():
        return []
    import pyarrow.parquet as pq
    return pq.read_table(path).to_pylist()


def clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def top_votes(field: str, labels: dict, n: int = 3) -> str:
    """'tid:votes:pct;...' -> 'label (pct%), ...'"""
    out = []
    for item in (field or "").split(";")[:n]:
        parts = item.split(":")
        if len(parts) == 3:
            out.append(f"{labels.get(parts[0], parts[0])} ({float(parts[2]):.0f}%)")
    return ", ".join(out)


def fmt_pros_cons(s: str) -> list[str]:
    """'pros(text,likes,dislikes;...)cons(...)' -> listas legibles."""
    out = []
    for kind, body in re.findall(r"(pros|cons)\((.*?)\)(?=cons\(|$)", s or "", flags=re.S):
        out.append(f"{kind.capitalize()}:")
        out += [f"- {item.rsplit(',', 2)[0]}" for item in body.split(";") if item]
    return out


def parse_notes(pyramid: str, notes: dict) -> list[str]:
    lines = []
    for level, body in re.findall(r"(\w+)\((.*?)\)", pyramid or ""):
        names = []
        for item in body.split(";"):
            name = notes.get(item.split(",")[0])
            if name and name not in names:
                names.append(name)
        if names:
            lines.append(f"- {level.capitalize()} notes: {', '.join(names)}")
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(ROOT.parent / "fragrance-database" / "samples"))
    ap.add_argument("--out", default=str(ROOT / "data"))
    ap.add_argument("--limit", type=int, default=0, help="máx. perfumes (los de más votos)")
    a = ap.parse_args()
    src, out = Path(a.src), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    labels = {r["id"]: r["en"] for r in read_csv(src / "translations.csv")}
    accords = {r["id"]: r["name"] for r in read_csv(src / "accords.csv")}
    notes_rows = read_csv(src / "notes.csv")
    notes = {r["id"]: r["name"] for r in notes_rows}
    frags = read_csv(src / "fragrances.csv")

    def votes(r):
        try:
            return int(r["rating"].split(";")[1])
        except (IndexError, ValueError):
            return 0

    if a.limit:
        frags = sorted(frags, key=votes, reverse=True)[: a.limit]
    pids = {r["pid"] for r in frags}

    reviews: dict[str, list[dict]] = {}
    for c in read_parquet(src / "comments_sample.parquet") or read_parquet(src / "comments.parquet"):
        if c["pid"] in pids and c["lang"] == "en":
            reviews.setdefault(c["pid"], []).append(c)

    # --- un documento por perfume ---
    (out / "fragrances").mkdir(exist_ok=True)
    for r in frags:
        brand = r["brand"].split(";")[0]
        perf = r["perfumers"].split(";")[0::2]
        rating = r["rating"].split(";")
        acc = [accords[x.split(":")[0]] for x in r["accords"].split(";") if x.split(":")[0] in accords]
        md = [f"# {r['name']} by {brand}", "",
              f"- Brand: {brand}", f"- Year: {r['year'] or 'unknown'}",
              f"- Target gender: {labels.get(r['gender'], r['gender'])}"]
        if perf and perf[0]:
            md.append(f"- Perfumer(s): {', '.join(perf)}")
        if acc:
            md.append(f"- Main accords: {', '.join(acc)}")
        md += parse_notes(r["notes_pyramid"], notes)
        if len(rating) == 2:
            md.append(f"- Community rating: {rating[0]} / 5 from {rating[1]} votes")
        for key, title in [("longevity", "Longevity"), ("sillage", "Sillage"), ("season", "Best seasons"),
                           ("time_of_day", "Time of day"), ("price_value", "Price perception")]:
            v = top_votes(r[key], labels, 2)
            if v:
                md.append(f"- {title} (community votes): {v}")
        md += ["", "## Description", "", clean(r["description"])]
        if r["pros_cons"]:
            md += ["", "## Pros and cons (community)", ""] + fmt_pros_cons(r["pros_cons"])
        if r["pid"] in reviews:
            md += ["", "## User reviews", ""]
            md += [f"- ({c['date']}, {c['author']}) {clean(c['text'])}" for c in reviews[r["pid"]]]
        (out / "fragrances" / f"{r['pid']}-{slug(r['name'])}.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # --- documentos de referencia ---
    ref = ["# Fragrance notes reference", ""]
    for r in notes_rows:
        ref += [f"## {r['name']}", f"Group: {r['group']}. Latin name: {r['latin_name'] or 'n/a'}.",
                clean(r["odor_profile"]), ""]
    (out / "notes.md").write_text("\n".join(ref), encoding="utf-8")

    brands = ["# Fragrance brands", ""]
    for r in read_csv(src / "brands.csv"):
        brands += [f"## {r['name']}", f"Country: {r['country']}. Activity: {r['main_activity']}. "
                   f"Parent company: {r['parent_company'] or 'none'}.", clean(r["description"]), ""]
    (out / "brands.md").write_text("\n".join(brands), encoding="utf-8")

    pf = ["# Perfumers (noses)", ""]
    for r in read_csv(src / "perfumers.csv"):
        pf += [f"## {r['name']}", f"Status: {r['status']}. Company: {r['company'] or 'n/a'}. "
               f"Perfumes created: {r['perfumes_count']}.", clean(r["biography"]), ""]
    (out / "perfumers.md").write_text("\n".join(pf), encoding="utf-8")

    # --- noticias ---
    (out / "news").mkdir(exist_ok=True)
    for n in read_parquet(src / "news_sample.parquet") or read_parquet(src / "news.parquet"):
        body = clean(n["text"])
        if len(body.split()) < 50:
            continue
        (out / "news" / f"{n['nid']}-{slug(n['title'])[:50]}.md").write_text(
            f"# {n['title']}\n\nCategory: {n['category']}. Author: {n['author']}.\n\n{body}\n", encoding="utf-8")

    files = list(out.rglob("*.md"))
    words = sum(len(f.read_text(encoding="utf-8").split()) for f in files)
    print(f"{len(files)} documentos, {words} palabras en {out}")


if __name__ == "__main__":
    main()
