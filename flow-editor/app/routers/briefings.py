from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import Briefing, Project
from app.schemas import BriefingCreate

router = APIRouter()


@router.post("/{project_id}")
def save_briefing(project_id: int, data: BriefingCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    existing = db.query(Briefing).filter(Briefing.project_id == project_id).order_by(Briefing.id.desc()).first()
    if existing:
        for key, val in data.model_dump(exclude_none=True).items():
            setattr(existing, key, val)
        existing.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        return {"id": existing.id, "ok": True}

    briefing = Briefing(project_id=project_id, **data.model_dump())
    db.add(briefing)
    db.commit()
    db.refresh(briefing)
    return {"id": briefing.id, "ok": True}


@router.get("/{project_id}")
def get_briefing(project_id: int, db: Session = Depends(get_db)):
    briefing = db.query(Briefing).filter(Briefing.project_id == project_id).order_by(Briefing.id.desc()).first()
    if not briefing:
        return {}
    return {
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
    }
