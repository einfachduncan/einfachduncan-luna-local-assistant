import json
import os
from datetime import datetime
from config import EXPORT_DIR

os.makedirs(EXPORT_DIR, exist_ok=True)


def export_chat(history):
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(EXPORT_DIR, f"chat_{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    return path
