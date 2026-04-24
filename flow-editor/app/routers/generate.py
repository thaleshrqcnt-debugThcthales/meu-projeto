from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import Project, Edict, Briefing, ProjectSection, Budget, Schedule
from app.config import settings
from app.schemas import SectionUpdate, HumanizeRequest

router = APIRouter()


def _require_api_key():
    if not settings.has_api_key():
        raise HTTPException(
            status_code=400,
            detail="API key não configurada. Acesse Configurações e insira sua ANTHROPIC_API_KEY."
        )


@router.post("/{project_id}/project")
def generate_project(project_id: int, db: Session = Depends(get_db)):
    """Gera todas as seções do projeto via IA."""
    _require_api_key()

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    briefing = db.query(Briefing).filter(Briefing.project_id == project_id).order_by(Briefing.id.desc()).first()
    edict = db.query(Edict).filter(Edict.project_id == project_id).order_by(Edict.id.desc()).first()
    edital_json = edict.extracted_json if edict else {}

    from app.services.project_generator import generate_project as gen
    sections_dict = gen(project, briefing, edital_json)

    # Salva ou atualiza seções no banco
    for section_name, content in sections_dict.items():
        existing = db.query(ProjectSection).filter(
            ProjectSection.project_id == project_id,
            ProjectSection.section_name == section_name
        ).first()
        if existing:
            existing.content = content
            existing.version += 1
            existing.updated_at = datetime.utcnow()
        else:
            sec = ProjectSection(
                project_id=project_id,
                section_name=section_name,
                content=content,
                version=1,
            )
            db.add(sec)

    project.status = "gerado"
    project.updated_at = datetime.utcnow()
    db.commit()

    return {
        "ok": True,
        "sections_generated": list(sections_dict.keys()),
        "message": "Projeto gerado com sucesso. Revise cada seção antes de exportar.",
    }


@router.post("/{project_id}/section/{section_name}")
def regenerate_section(project_id: int, section_name: str, db: Session = Depends(get_db)):
    """Regenera uma seção específica."""
    _require_api_key()

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    briefing = db.query(Briefing).filter(Briefing.project_id == project_id).order_by(Briefing.id.desc()).first()
    edict = db.query(Edict).filter(Edict.project_id == project_id).order_by(Edict.id.desc()).first()
    edital_json = edict.extracted_json if edict else {}

    from app.services.project_generator import generate_single_section
    content = generate_single_section(project, briefing, edital_json, section_name)

    existing = db.query(ProjectSection).filter(
        ProjectSection.project_id == project_id,
        ProjectSection.section_name == section_name
    ).first()
    if existing:
        existing.content = content
        existing.version += 1
        existing.updated_at = datetime.utcnow()
    else:
        sec = ProjectSection(project_id=project_id, section_name=section_name, content=content)
        db.add(sec)

    db.commit()
    return {"ok": True, "section_name": section_name, "content": content}


@router.put("/{project_id}/section")
def update_section(project_id: int, data: SectionUpdate, db: Session = Depends(get_db)):
    """Atualiza manualmente uma seção."""
    existing = db.query(ProjectSection).filter(
        ProjectSection.project_id == project_id,
        ProjectSection.section_name == data.section_name
    ).first()
    if existing:
        existing.content = data.content
        existing.version += 1
        existing.updated_at = datetime.utcnow()
    else:
        sec = ProjectSection(
            project_id=project_id,
            section_name=data.section_name,
            content=data.content,
        )
        db.add(sec)
    db.commit()
    return {"ok": True}


@router.post("/humanize")
def humanize_text(data: HumanizeRequest):
    """Reescreve trecho com linguagem cultural técnica."""
    _require_api_key()
    from app.services.humanizer import humanize
    result = humanize(data.text, data.mode, data.section_context or "")
    return {"result": result}


@router.post("/{project_id}/budget")
def save_budget(project_id: int, items: list = Body(...), db: Session = Depends(get_db)):
    """Salva itens de orçamento."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    # Remove orçamento existente e recria
    db.query(Budget).filter(Budget.project_id == project_id).delete()

    for item in items:
        qty = float(item.get("quantity", 1))
        unit_val = float(item.get("unit_value", 0))
        b = Budget(
            project_id=project_id,
            item=item.get("item", ""),
            category=item.get("category", ""),
            description=item.get("description", ""),
            unit=item.get("unit", ""),
            quantity=qty,
            unit_value=unit_val,
            total_value=qty * unit_val,
            justification=item.get("justification", ""),
            related_action=item.get("related_action", ""),
        )
        db.add(b)

    db.commit()
    return {"ok": True, "items_saved": len(items)}


@router.post("/{project_id}/schedule")
def save_schedule(project_id: int, items: list = Body(...), db: Session = Depends(get_db)):
    """Salva cronograma."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    db.query(Schedule).filter(Schedule.project_id == project_id).delete()

    for item in items:
        s = Schedule(
            project_id=project_id,
            phase=item.get("phase", ""),
            month=item.get("month", ""),
            activity=item.get("activity", ""),
            responsible=item.get("responsible", ""),
            evidence=item.get("evidence", ""),
        )
        db.add(s)

    db.commit()
    return {"ok": True}


@router.get("/{project_id}/sections")
def get_sections(project_id: int, db: Session = Depends(get_db)):
    sections = db.query(ProjectSection).filter(ProjectSection.project_id == project_id).all()
    return [
        {"id": s.id, "section_name": s.section_name, "content": s.content, "version": s.version}
        for s in sections
    ]
