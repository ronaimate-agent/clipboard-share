import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Clipboard Share")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.environ.get("DB_PATH", "/data/clipboard.db")


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


class SnippetCreate(BaseModel):
    content: str


class SnippetResponse(BaseModel):
    id: int
    content: str
    created_at: str


@app.on_event("startup")
def startup():
    init_db()


@app.get("/api/snippets", response_model=list[SnippetResponse])
def list_snippets():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, content, created_at FROM snippets ORDER BY created_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]


@app.post("/api/snippets", response_model=SnippetResponse, status_code=201)
def create_snippet(snippet: SnippetCreate):
    if not snippet.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO snippets (content, created_at) VALUES (?, ?)",
            (snippet.content.strip(), now),
        )
        snippet_id = cursor.lastrowid
    return {"id": snippet_id, "content": snippet.content.strip(), "created_at": now}


@app.delete("/api/snippets/{snippet_id}", status_code=204)
def delete_snippet(snippet_id: int):
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM snippets WHERE id = ?", (snippet_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Snippet not found")


app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
