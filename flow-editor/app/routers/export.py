import os
from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project, ProjectSection, Budget, Schedule, Edict, Audit, ScoreSimulation, Export
from app.config import settings

router = APIRouter()


def _safe_name(text: str) -> str:
    return "".join(c for c in text if c.isalnum() or c in " _-")[:40].strip().replace(" ", "_")


def _get_export_dir(project_id: int) -> Path:
    p = settings.get_exports_path() / str(project_id)
    p.mkdir(parents=True, exist_ok=True)
    return p


def _get_project_data(project_id: int, db: Session):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    sections = db.query(ProjectSection).filter(ProjectSection.project_id == project_id).all()
    budgets = db.query(Budget).filter(Budget.project_id == project_id).all()
    schedules = db.query(Schedule).filter(Schedule.project_id == project_id).all()
    return project, sections, budgets, schedules


def _log_export(project_id: int, file_type: str, file_path: str, db: Session):
    exp = Export(project_id=project_id, file_type=file_type, file_path=file_path)
    db.add(exp)
    db.commit()


@router.get("/{project_id}/docx")
def export_docx(project_id: int, db: Session = Depends(get_db)):
    project, sections, budgets, schedules = _get_project_data(project_id, db)
    export_dir = _get_export_dir(project_id)
    file_path = str(export_dir / f"projeto_{_safe_name(project.internal_name)}.docx")

    from app.services.docx_exporter import export_project_docx
    export_project_docx(project, sections, budgets, schedules, file_path)
    _log_export(project_id, "docx", file_path, db)

    return FileResponse(
        path=file_path,
        filename=f"projeto_{_safe_name(project.internal_name)}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@router.get("/{project_id}/xlsx")
def export_xlsx(project_id: int, db: Session = Depends(get_db)):
    project, sections, budgets, schedules = _get_project_data(project_id, db)
    export_dir = _get_export_dir(project_id)
    file_path = str(export_dir / f"orcamento_{_safe_name(project.internal_name)}.xlsx")

    from app.services.xlsx_exporter import export_budget_xlsx
    export_budget_xlsx(project, budgets, file_path)
    _log_export(project_id, "xlsx", file_path, db)

    return FileResponse(
        path=file_path,
        filename=f"orcamento_{_safe_name(project.internal_name)}.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@router.get("/{project_id}/audit-docx")
def export_audit_docx(project_id: int, db: Session = Depends(get_db)):
    project, sections, budgets, schedules = _get_project_data(project_id, db)
    audit = db.query(Audit).filter(Audit.project_id == project_id).order_by(Audit.id.desc()).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Nenhuma auditoria encontrada. Execute a auditoria primeiro.")

    export_dir = _get_export_dir(project_id)
    file_path = str(export_dir / "relatorio_auditoria.docx")

    from app.services.docx_exporter import export_audit_docx as exp_audit
    exp_audit(audit.findings_json or {}, project, file_path)
    _log_export(project_id, "audit_docx", file_path, db)

    return FileResponse(
        path=file_path,
        filename="relatorio_auditoria.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@router.get("/{project_id}/score-docx")
def export_score_docx(project_id: int, db: Session = Depends(get_db)):
    project, sections, budgets, schedules = _get_project_data(project_id, db)
    sim = db.query(ScoreSimulation).filter(ScoreSimulation.project_id == project_id).order_by(ScoreSimulation.id.desc()).first()
    if not sim:
        raise HTTPException(status_code=404, detail="Nenhuma simulação encontrada. Execute a simulação de banca primeiro.")

    export_dir = _get_export_dir(project_id)
    file_path = str(export_dir / "parecer_banca_simulada.docx")

    score_data = {
        "c1_score": sim.c1_score,
        "c2_score": sim.c2_score,
        "c3_score": sim.c3_score,
        "c4_score": sim.c4_score,
        "c5_score": sim.c5_score,
        "total_score": sim.total_score,
        "competitive_range": sim.competitive_range,
        "opinion_text": sim.opinion_text,
        "recommendations": sim.recommendations_json or [],
    }

    from app.services.docx_exporter import export_score_docx as exp_score
    exp_score(score_data, project, file_path)
    _log_export(project_id, "score_docx", file_path, db)

    return FileResponse(
        path=file_path,
        filename="parecer_banca_simulada.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@router.get("/{project_id}/md")
def export_md(project_id: int, db: Session = Depends(get_db)):
    project, sections, budgets, schedules = _get_project_data(project_id, db)
    export_dir = _get_export_dir(project_id)
    file_path = str(export_dir / f"projeto_{_safe_name(project.internal_name)}.md")

    from app.services.zip_exporter import export_project_md
    export_project_md(project, sections, file_path)
    _log_export(project_id, "md", file_path, db)

    return FileResponse(
        path=file_path,
        filename=f"projeto_{_safe_name(project.internal_name)}.md",
        media_type="text/markdown",
    )


@router.get("/{project_id}/zip")
def export_zip(project_id: int, db: Session = Depends(get_db)):
    project, sections, budgets, schedules = _get_project_data(project_id, db)
    export_dir = _get_export_dir(project_id)

    # Gera todos os arquivos necessários
    safe = _safe_name(project.internal_name)

    docx_path = str(export_dir / f"projeto_{safe}.docx")
    xlsx_path = str(export_dir / f"orcamento_{safe}.xlsx")
    audit_path = str(export_dir / "relatorio_auditoria.docx")
    score_path = str(export_dir / "parecer_banca_simulada.docx")
    md_path = str(export_dir / f"projeto_{safe}.md")
    zip_path = str(export_dir / f"pacote_final_{safe}_{datetime.now().strftime('%Y%m%d')}.zip")

    from app.services.docx_exporter import export_project_docx, export_audit_docx, export_score_docx
    from app.services.xlsx_exporter import export_budget_xlsx
    from app.services.zip_exporter import export_project_md, create_package_zip

    export_project_docx(project, sections, budgets, schedules, docx_path)
    export_budget_xlsx(project, budgets, xlsx_path)
    export_project_md(project, sections, md_path)

    audit = db.query(Audit).filter(Audit.project_id == project_id).order_by(Audit.id.desc()).first()
    if audit:
        export_audit_docx(audit.findings_json or {}, project, audit_path)

    sim = db.query(ScoreSimulation).filter(ScoreSimulation.project_id == project_id).order_by(ScoreSimulation.id.desc()).first()
    if sim:
        score_data = {
            "c1_score": sim.c1_score, "c2_score": sim.c2_score,
            "c3_score": sim.c3_score, "c4_score": sim.c4_score,
            "c5_score": sim.c5_score, "total_score": sim.total_score,
            "competitive_range": sim.competitive_range,
            "opinion_text": sim.opinion_text,
            "recommendations": sim.recommendations_json or [],
        }
        export_score_docx(score_data, project, score_path)

    create_package_zip(
        project,
        docx_path=docx_path if Path(docx_path).exists() else None,
        xlsx_path=xlsx_path if Path(xlsx_path).exists() else None,
        audit_docx_path=audit_path if Path(audit_path).exists() else None,
        score_docx_path=score_path if Path(score_path).exists() else None,
        md_path=md_path if Path(md_path).exists() else None,
        output_path=zip_path,
    )

    _log_export(project_id, "zip", zip_path, db)

    return FileResponse(
        path=zip_path,
        filename=f"pacote_final_{safe}.zip",
        media_type="application/zip",
    )
