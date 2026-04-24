from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import Project, Edict, ProjectSection, Budget, Schedule, Audit, ScoreSimulation, Briefing
from app.config import settings

router = APIRouter()


def _get_project_data(project_id: int, db: Session):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    sections = db.query(ProjectSection).filter(ProjectSection.project_id == project_id).all()
    budgets = db.query(Budget).filter(Budget.project_id == project_id).all()
    schedules = db.query(Schedule).filter(Schedule.project_id == project_id).all()
    edict = db.query(Edict).filter(Edict.project_id == project_id).order_by(Edict.id.desc()).first()
    briefing = db.query(Briefing).filter(Briefing.project_id == project_id).order_by(Briefing.id.desc()).first()
    edital_json = edict.extracted_json if edict else {}
    return project, sections, budgets, schedules, edital_json, briefing


@router.post("/{project_id}/consistency")
def run_consistency_audit(project_id: int, db: Session = Depends(get_db)):
    """Executa auditoria determinística de coerência (sem IA)."""
    project, sections, budgets, schedules, edital_json, briefing = _get_project_data(project_id, db)

    from app.services.consistency_auditor import run_full_audit
    result = run_full_audit(project, sections, budgets)

    audit = Audit(
        project_id=project_id,
        audit_type="coerencia_deterministica",
        score=result["score"],
        status=result["status"],
        findings_json=result,
    )
    db.add(audit)
    db.commit()

    return result


@router.post("/{project_id}/ai-consistency")
def run_ai_consistency_audit(project_id: int, db: Session = Depends(get_db)):
    """Executa auditoria de coerência via IA (complementar à determinística)."""
    if not settings.has_api_key():
        raise HTTPException(status_code=400, detail="API key não configurada")

    project, sections, budgets, schedules, edital_json, briefing = _get_project_data(project_id, db)

    from app.services.ai_provider import ai_provider, load_prompt
    import json

    sections_text = "\n\n".join(
        f"## {s.section_name}\n{s.content or ''}" for s in sections if s.content
    )[:30000]

    budget_data = "\n".join(
        f"- {b.item}: {b.quantity}x R${b.unit_value} = R${b.total_value}"
        for b in budgets
    )

    schedule_data = "\n".join(
        f"- {s.phase} | {s.month}: {s.activity}" for s in schedules
    )

    project_data = json.dumps({
        "nome": project.public_title or project.internal_name,
        "proponente": project.proponent_name,
        "modulo": project.selected_module,
        "valor": project.intended_budget,
        "duracao": project.duration_months,
        "linguagem": project.cultural_language,
        "modalidade": project.modality,
    }, ensure_ascii=False)

    prompt_template = load_prompt("auditar_coerencia.md")
    prompt = (
        prompt_template
        .replace("{project_data}", project_data)
        .replace("{sections_text}", sections_text)
        .replace("{budget_data}", budget_data)
        .replace("{schedule_data}", schedule_data)
        .replace("{edital_json}", json.dumps(edital_json, ensure_ascii=False, indent=2))
    )

    try:
        result = ai_provider.complete_json(prompt, max_tokens=6000)
    except Exception as e:
        result = {
            "score": 0,
            "status": "ERRO",
            "findings": [],
            "summary": f"Erro na auditoria IA: {e}",
        }

    result["source"] = "ai"
    audit = Audit(
        project_id=project_id,
        audit_type="coerencia_ia",
        score=result.get("score", 0),
        status=result.get("status", ""),
        findings_json=result,
    )
    db.add(audit)
    db.commit()

    return result


@router.post("/{project_id}/score")
def simulate_score(project_id: int, db: Session = Depends(get_db)):
    """Simula parecer de banca."""
    if not settings.has_api_key():
        raise HTTPException(status_code=400, detail="API key não configurada")

    project, sections, budgets, schedules, edital_json, briefing = _get_project_data(project_id, db)

    from app.agents.agente_parecerista import avaliar
    result = avaliar(project, sections, budgets, schedules, edital_json)

    sim = ScoreSimulation(
        project_id=project_id,
        c1_score=result.get("c1_score", 0),
        c2_score=result.get("c2_score", 0),
        c3_score=result.get("c3_score", 0),
        c4_score=result.get("c4_score", 0),
        c5_score=result.get("c5_score", 0),
        total_score=result.get("total_score", 0),
        competitive_range=result.get("competitive_range", ""),
        opinion_text=result.get("opinion_text", ""),
        recommendations_json=result.get("recommendations", []),
    )
    db.add(sim)
    db.commit()

    return result


@router.post("/{project_id}/risks")
def detect_risks(project_id: int, db: Session = Depends(get_db)):
    """Detecta riscos formais de desclassificação."""
    project, sections, budgets, schedules, edital_json, briefing = _get_project_data(project_id, db)

    from app.agents.agente_risco_formal import detectar_riscos
    return detectar_riscos(project, sections, budgets, edital_json)


@router.post("/{project_id}/accessibility")
def check_accessibility(project_id: int, db: Session = Depends(get_db)):
    """Verifica plano de acessibilidade."""
    project, sections, budgets, schedules, edital_json, briefing = _get_project_data(project_id, db)

    from app.agents.agente_acessibilidade import verificar
    return verificar(sections, budgets, edital_json)


@router.post("/{project_id}/territory")
def check_territory(project_id: int, db: Session = Depends(get_db)):
    """Analisa coerência territorial."""
    project, sections, budgets, schedules, edital_json, briefing = _get_project_data(project_id, db)

    from app.agents.agente_territorio import analisar
    return analisar(sections, briefing)


@router.post("/{project_id}/budget-audit")
def audit_budget(project_id: int, db: Session = Depends(get_db)):
    """Audita orçamento via IA."""
    if not settings.has_api_key():
        raise HTTPException(status_code=400, detail="API key não configurada")

    project, sections, budgets, schedules, edital_json, briefing = _get_project_data(project_id, db)

    from app.agents.agente_orcamentista import auditar_orcamento
    return auditar_orcamento(project, budgets, sections, edital_json)


@router.post("/{project_id}/checklist")
def generate_checklist(project_id: int, db: Session = Depends(get_db)):
    """Gera checklist documental."""
    if not settings.has_api_key():
        raise HTTPException(status_code=400, detail="API key não configurada")

    project, sections, budgets, schedules, edital_json, briefing = _get_project_data(project_id, db)

    from app.agents.agente_documental import gerar_checklist
    return gerar_checklist(project, edital_json)


@router.get("/{project_id}/history")
def get_audit_history(project_id: int, db: Session = Depends(get_db)):
    audits = db.query(Audit).filter(Audit.project_id == project_id).order_by(Audit.id.desc()).limit(10).all()
    return [
        {
            "id": a.id,
            "audit_type": a.audit_type,
            "score": a.score,
            "status": a.status,
            "created_at": str(a.created_at),
        }
        for a in audits
    ]
