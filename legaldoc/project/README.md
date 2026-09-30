# PocketSmart AI

Complete FastAPI + Jinja2 + SQLite + Gemini implementation based on the supplied PocketSmart AI documentation.

## Setup
1. Install Python 3.11+.
2. Open this folder in VS Code.
3. Create environment: `python -m venv .venv`
4. Windows: `.venv\\Scripts\\activate`
5. Install: `pip install -r requirements.txt`
6. Copy `.env.example` to `.env`.
7. Put your Gemini API key in `GEMINI_API_KEY`.
8. Run: `uvicorn app.main:app --reload`
9. Open `http://127.0.0.1:8000`.
10. API docs: `http://127.0.0.1:8000/docs`.

The source document names Gemini 1.5 Flash Pro, while this implementation defaults to `gemini-2.5-flash`; change `GEMINI_MODEL` if your account provides another supported model. If no key is configured, fallback recommendations keep the application runnable.

## Main endpoints
`POST /api/register`, `POST /api/login`, `POST /api/logout`, `GET /api/token`, `GET /api/session-info`, `GET /api/session-data`, `POST /api/generate-home`, `POST /api/generate-party`, `POST /api/generate-jewelry`, `GET /api/history`, `GET /api/recommendations-details/{history_id}`.
