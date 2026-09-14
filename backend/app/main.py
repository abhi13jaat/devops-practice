"""FastAPI application for the DevOps Task Manager."""

import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import Task, TaskCreate

# Load environment variables from .env (if present)
load_dotenv()

# ─── Configuration (read from environment) ─────────────────────
APP_ENV = os.getenv("APP_ENV", "development")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# ─── Application ───────────────────────────────────────────────
app = FastAPI(
    title="DevOps Task Manager API",
    version="0.2.0",
    description="Backend for the DevOps Task Manager learning project.",
)

# CORS: allow the React dev server to call this API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── In-memory storage (replaced by PostgreSQL in a later phase) ─
_tasks: List[Task] = []
_next_id = 1


# ─── Routes ────────────────────────────────────────────────────
@app.get("/health")
def health():
    """Liveness check — used by orchestrators later."""
    return {"status": "ok", "env": APP_ENV}


@app.get("/api/tasks", response_model=List[Task])
def list_tasks():
    """Return all tasks."""
    return _tasks


@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    """Create a new task."""
    global _next_id
    task = Task(id=_next_id, title=payload.title, description=payload.description)
    _tasks.append(task)
    _next_id += 1
    return task


@app.get("/api/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Get a single task by ID."""
    for t in _tasks:
        if t.id == task_id:
            return t
    raise HTTPException(status_code=404, detail="Task not found")
