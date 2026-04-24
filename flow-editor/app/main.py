from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
import logging

from app.config import settings
from app.database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FLOW EDITOR",
    description="Sistema Operacional de Projetos Culturais",
    version="1.0.0",
)

BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Import and register routers
from app.routers import projects, edicts, briefings, generate, audit, export, settings as settings_router

app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(edicts.router, prefix="/api/edicts", tags=["edicts"])
app.include_router(briefings.router, prefix="/api/briefings", tags=["briefings"])
app.include_router(generate.router, prefix="/api/generate", tags=["generate"])
app.include_router(audit.router, prefix="/api/audit", tags=["audit"])
app.include_router(export.router, prefix="/api/export", tags=["export"])
app.include_router(settings_router.router, prefix="/api/settings", tags=["settings"])

# Page routes
from app.routers import pages
app.include_router(pages.router, tags=["pages"])


@app.on_event("startup")
async def startup_event():
    logger.info("Iniciando FLOW EDITOR...")
    init_db()
    settings.get_exports_path()
    settings.get_uploads_path()
    logger.info(f"Banco de dados: {settings.database_url}")
    logger.info(f"API Key configurada: {settings.has_api_key()}")
    logger.info("FLOW EDITOR pronto em http://127.0.0.1:8000")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": "1.0.0",
        "api_key_configured": settings.has_api_key(),
        "ai_model": settings.ai_model,
    }
