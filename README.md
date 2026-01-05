# Habit Bunnies

Playful habit tracker with a FastAPI + SQLModel backend and a React + Vite + Tailwind frontend.

## Project layout
- `backend/` — FastAPI app (`backend/app`)
- `frontend/` — React + Vite UI
- `.gitignore`, `README.md`

## Backend (FastAPI)

1) Install deps (once): `uv pip install fastapi sqlmodel uvicorn`
2) Run API from repo root: `uv run uvicorn backend.app.api:app --reload`
   - Serves at http://localhost:8000
   - SQLite file: `habits.db` (auto-created)
   - Compatibility: `uv run uvicorn app.api:app --reload` also works (wrapper points to backend/app)

## Frontend (React + Vite)

1) `cd frontend`
2) Install deps: `npm install` (or `pnpm install`)
3) Run dev server: `VITE_API_BASE=http://localhost:8000 npm run dev`
   - Opens http://localhost:5173 (CORS is enabled in the API for this origin)

## Notes

- API endpoints are documented in `backend/app/api.py`.
- Models and DB setup live in `backend/app/models.py` and `backend/app/db.py`.
- Tailwind theme and bunny styling in `frontend/src/index.css` and `frontend/tailwind.config.js`.
