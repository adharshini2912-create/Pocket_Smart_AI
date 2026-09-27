# PocketSmart AI

Complete FastAPI + Jinja2 + Google Gemini budget/recommendation application based on the supplied documentation.

## Features
- Registration, login, logout and JWT-protected APIs
- Home, Party and Jewelry budget planners
- Optional outfit-image analysis for Jewelry
- Gemini-powered structured recommendations
- Deterministic fallback recommendations when Gemini is not configured/unavailable
- SQLite storage for users and recommendation history
- Responsive frontend
- API and unit tests

The documentation names Gemini 1.5 Flash Pro. The model is configurable through `GEMINI_MODEL`; the example uses `gemini-2.5-flash`. Change it to a model available to your API account if required.

## Windows PowerShell setup
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# edit .env and add GEMINI_API_KEY
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000

## Test
```powershell
pytest -q
```
API docs: http://127.0.0.1:8000/docs

External marketplaces from the documentation are represented as search links rather than scraped/live product APIs. This prevents fake prices and brittle scraping.
