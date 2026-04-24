from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import Project
from app.schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from typing import List

router = APIRouter()


@router.get("/", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.updated_at.desc()).all()


@router.post("/", response_model=ProjectResponse)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(**data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return p


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, data: ProjectUpdate, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    for key, val in data.model_dump(exclude_none=True).items():
        setattr(p, key, val)
    p.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(p)
    return p


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    db.delete(p)
    db.commit()
    return {"ok": True}


@router.get("/{project_id}/full")
def get_project_full(project_id: int, db: Session = Depends(get_db)):
    """Retorna projeto com todas as seções, orçamento, cronograma, edital e auditorias."""
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    from app.models import ProjectSection, Budget, Schedule, Edict, Audit, ScoreSimulation, Briefing

    sections = db.query(ProjectSection).filter(ProjectSection.project_id == project_id).all()
    budgets = db.query(Budget).filter(Budget.project_id == project_id).all()
    schedules = db.query(Schedule).filter(Schedule.project_id == project_id).all()
    edict = db.query(Edict).filter(Edict.project_id == project_id).order_by(Edict.id.desc()).first()
    audits = db.query(Audit).filter(Audit.project_id == project_id).order_by(Audit.id.desc()).all()
    scores = db.query(ScoreSimulation).filter(ScoreSimulation.project_id == project_id).order_by(ScoreSimulation.id.desc()).all()
    briefing = db.query(Briefing).filter(Briefing.project_id == project_id).order_by(Briefing.id.desc()).first()

    return {
        "project": {
            "id": p.id,
            "internal_name": p.internal_name,
            "public_title": p.public_title,
            "proponent_name": p.proponent_name,
            "proponent_type": p.proponent_type,
            "city": p.city,
            "state": p.state,
            "cultural_language": p.cultural_language,
            "modality": p.modality,
            "selected_module": p.selected_module,
            "intended_budget": p.intended_budget,
            "duration_months": p.duration_months,
            "observations": p.observations,
            "status": p.status,
            "created_at": str(p.created_at),
            "updated_at": str(p.updated_at),
        },
        "sections": [
            {"id": s.id, "section_name": s.section_name, "content": s.content, "version": s.version}
            for s in sections
        ],
        "budgets": [
            {"id": b.id, "item": b.item, "category": b.category, "description": b.description,
             "unit": b.unit, "quantity": b.quantity, "unit_value": b.unit_value,
             "total_value": b.total_value, "justification": b.justification, "related_action": b.related_action}
            for b in budgets
        ],
        "schedules": [
            {"id": s.id, "phase": s.phase, "month": s.month, "activity": s.activity,
             "responsible": s.responsible, "evidence": s.evidence}
            for s in schedules
        ],
        "edict": {
            "id": edict.id,
            "filename": edict.filename,
            "page_count": edict.page_count,
            "extraction_status": edict.extraction_status,
            "extracted_json": edict.extracted_json,
        } if edict else None,
        "latest_audit": {
            "score": audits[0].score,
            "status": audits[0].status,
            "findings": audits[0].findings_json,
        } if audits else None,
        "latest_score": {
            "total_score": scores[0].total_score,
            "competitive_range": scores[0].competitive_range,
        } if scores else None,
        "briefing": {
            "free_text": briefing.free_text,
            "territory": briefing.territory,
            "target_audience": briefing.target_audience,
            "team_artists": briefing.team_artists,
            "planned_actions": briefing.planned_actions,
            "desired_spaces": briefing.desired_spaces,
            "cultural_references": briefing.cultural_references,
            "confirmed_partners": briefing.confirmed_partners,
            "desired_partners": briefing.desired_partners,
            "proponent_history": briefing.proponent_history,
            "needed_materials": briefing.needed_materials,
            "desired_accessibility": briefing.desired_accessibility,
            "desired_counterpart": briefing.desired_counterpart,
        } if briefing else None,
    }
