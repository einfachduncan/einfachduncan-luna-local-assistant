import os
from duckduckgo_search import DDGS
from config import FILES_DIR

os.makedirs(FILES_DIR, exist_ok=True)


def web_search(query: str, max_results: int = 5) -> str:
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append(r)

    if not results:
        return "Keine Suchergebnisse gefunden."

    lines = []
    for i, r in enumerate(results, start=1):
        lines.append(
            f"{i}. {r.get('title', 'Ohne Titel')}\n"
            f"   URL: {r.get('href', '')}\n"
            f"   Snippet: {r.get('body', '')}"
        )
    return "\n\n".join(lines)


def list_files() -> str:
    collected = []
    for root, _, files in os.walk(FILES_DIR):
        for file in files:
            full = os.path.join(root, file)
            rel = os.path.relpath(full, FILES_DIR)
            collected.append(rel)
    if not collected:
        return "Keine Dateien gefunden."
    return "\n".join(sorted(collected))


def read_file(path: str) -> str:
    full = os.path.abspath(os.path.join(FILES_DIR, path))
    base = os.path.abspath(FILES_DIR)
    if not full.startswith(base):
        return "Ungültiger Pfad."
    if not os.path.exists(full):
        return "Datei nicht gefunden."
    with open(full, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str) -> str:
    full = os.path.abspath(os.path.join(FILES_DIR, path))
    base = os.path.abspath(FILES_DIR)
    if not full.startswith(base):
        return "Ungültiger Pfad."
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Gespeichert unter: {path}"