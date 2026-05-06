import os
import sqlite3
from typing import List, Dict

from config import SQLITE_PATH, DATA_DIR

os.makedirs(DATA_DIR, exist_ok=True)


class MemoryStore:
    def __init__(self, db_path: str = SQLITE_PATH):
        self.db_path = db_path
        self._init_db()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kind TEXT NOT NULL,
                    content TEXT NOT NULL,
                    meta TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def add(self, kind: str, content: str, meta: str = ""):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO memories (kind, content, meta) VALUES (?, ?, ?)",
                (kind, content, meta)
            )
            conn.commit()

    def recent(self, limit: int = 8) -> List[Dict]:
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT id, kind, content, meta, created_at
                FROM memories
                ORDER BY id DESC
                LIMIT ?
            """, (limit,)).fetchall()

        return [
            {"id": r[0], "kind": r[1], "content": r[2], "meta": r[3], "created_at": r[4]}
            for r in rows
        ]

    def search(self, query: str, limit: int = 6) -> List[Dict]:
        q = f"%{query}%"
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT id, kind, content, meta, created_at
                FROM memories
                WHERE content LIKE ? OR meta LIKE ?
                ORDER BY id DESC
                LIMIT ?
            """, (q, q, limit)).fetchall()

        return [
            {"id": r[0], "kind": r[1], "content": r[2], "meta": r[3], "created_at": r[4]}
            for r in rows
        ]
