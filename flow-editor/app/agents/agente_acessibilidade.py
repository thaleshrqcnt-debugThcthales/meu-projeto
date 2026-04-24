"""
Agente Acessibilidade: verifica se o projeto contempla acessibilidade adequada.
"""
from app.services.consistency_auditor import check_accessibility_budget


def verificar(sections: list, budgets: list, edital_json: dict) -> dict:
    """Verifica cobertura de acessibilidade."""
    findings = check_accessibility_budget(budgets, sections)

    access_section = next((s for s in sections if s.section_name == "PLANO_ACESSIBILIDADE"), None)
    access_text = access_section.content if access_section else ""

    checklist = {
        "arquitetonica": "arquitetôn" in access_text.lower() or "espaço acessív" in access_text.lower(),
        "comunicacional": "comunicacional" in access_text.lower() or "libras" in access_text.lower(),
        "atitudinal": "atitudinal" in access_text.lower() or "mediação" in access_text.lower(),
        "libras": "libras" in access_text.lower(),
        "audiodescricao": "audiodescri" in access_text.lower(),
        "materiais_acessiveis": "braille" in access_text.lower() or "material acessív" in access_text.lower(),
        "orcamento_correspondente": any(
            "acessibilidade" in (b.category or "").lower() or "libras" in (b.item or "").lower()
            for b in budgets
        ),
    }

    score = sum(1 for v in checklist.values() if v) / len(checklist) * 100

    return {
        "checklist": checklist,
        "score_acessibilidade": round(score, 1),
        "findings": [f.to_dict() if hasattr(f, "to_dict") else f for f in findings],
        "plano_existe": bool(access_text and len(access_text.strip()) > 100),
    }
