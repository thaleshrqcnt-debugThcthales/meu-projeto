from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from app.database import get_db
from app.models import Project, Audit, ScoreSimulation
from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.updated_at.desc()).limit(10).all()
    projects_data = []
    for p in projects:
        latest_audit = db.query(Audit).filter(Audit.project_id == p.id).order_by(Audit.id.desc()).first()
        latest_score = db.query(ScoreSimulation).filter(ScoreSimulation.project_id == p.id).order_by(ScoreSimulation.id.desc()).first()
        projects_data.append({
            "project": p,
            "audit_score": latest_audit.score if latest_audit else None,
            "audit_status": latest_audit.status if latest_audit else None,
            "sim_score": latest_score.total_score if latest_score else None,
            "sim_range": latest_score.competitive_range if latest_score else None,
        })
    return templates.TemplateResponse("index.html", {
        "request": request,
        "projects_data": projects_data,
        "api_configured": settings.has_api_key(),
        "ai_model": settings.ai_model,
    })


@router.get("/projeto/novo", response_class=HTMLResponse)
def new_project_page(request: Request):
    return templates.TemplateResponse("project_form.html", {"request": request, "project": None, "editing": False})


@router.get("/projeto/{project_id}", response_class=HTMLResponse)
def project_page(request: Request, project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        from fastapi.responses import RedirectResponse
        return RedirectResponse("/")
    return templates.TemplateResponse("project_detail.html", {
        "request": request,
        "project": project,
        "api_configured": settings.has_api_key(),
    })


@router.get("/projeto/{project_id}/editar", response_class=HTMLResponse)
def edit_project_page(request: Request, project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    return templates.TemplateResponse("project_form.html", {
        "request": request,
        "project": project,
        "editing": True,
    })


@router.get("/projeto/{project_id}/edital", response_class=HTMLResponse)
def edict_page(request: Request, project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    return templates.TemplateResponse("edital_view.html", {
        "request": request,
        "project": project,
        "api_configured": settings.has_api_key(),
    })


@router.get("/projeto/{project_id}/briefing", response_class=HTMLResponse)
def briefing_page(request: Request, project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    return templates.TemplateResponse("briefing_form.html", {
        "request": request,
        "project": project,
        "api_configured": settings.has_api_key(),
    })


@router.get("/projeto/{project_id}/gerar", response_class=HTMLResponse)
def generate_page(request: Request, project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    return templates.TemplateResponse("generate.html", {
        "request": request,
        "project": project,
        "api_configured": settings.has_api_key(),
    })


@router.get("/projeto/{project_id}/auditoria", response_class=HTMLResponse)
def audit_page(request: Request, project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    return templates.TemplateResponse("audit.html", {
        "request": request,
        "project": project,
        "api_configured": settings.has_api_key(),
    })


@router.get("/projeto/{project_id}/banca", response_class=HTMLResponse)
def score_page(request: Request, project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    return templates.TemplateResponse("score.html", {
        "request": request,
        "project": project,
        "api_configured": settings.has_api_key(),
    })


@router.get("/projeto/{project_id}/exportar", response_class=HTMLResponse)
def export_page(request: Request, project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    return templates.TemplateResponse("export.html", {
        "request": request,
        "project": project,
    })


@router.get("/configuracoes", response_class=HTMLResponse)
def settings_page(request: Request):
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "api_configured": settings.has_api_key(),
        "ai_model": settings.ai_model,
    })
