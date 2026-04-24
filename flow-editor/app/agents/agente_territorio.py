"""
Agente Território: analisa coerência territorial do projeto.
"""
import re


def analisar(sections: list, briefing=None) -> dict:
    diag = next((s.content or "" for s in sections if s.section_name == "DIAGNOSTICO_TERRITORIAL"), "")
    metod = next((s.content or "" for s in sections if s.section_name == "METODOLOGIA"), "")
    comm = next((s.content or "" for s in sections if s.section_name == "PLANO_COMUNICACAO"), "")

    territory = briefing.territory if briefing else ""

    checklist = {
        "territorio_na_justificativa": bool(territory and territory[:15].lower() in
                                            next((s.content or "" for s in sections if s.section_name == "JUSTIFICATIVA"), "").lower()),
        "territorio_no_diagnostico": bool(territory and len(diag) > 100),
        "territorio_na_metodologia": bool(territory and len(metod) > 100),
        "territorio_na_comunicacao": bool(territory and len(comm) > 50),
        "afirmacoes_fortes_marcadas": not bool(re.search(
            r"(maior índice|maior taxa|único espaço|ausência total|nenhum equipamento)",
            diag, re.I
        )),
    }

    findings = []
    if not checklist["territorio_na_justificativa"] and territory:
        findings.append({
            "level": "medio",
            "category": "territorio",
            "location": "JUSTIFICATIVA",
            "problem": "Território não mencionado na Justificativa",
            "impact": "Fragiliza a conexão entre o projeto e o contexto local",
            "suggestion": "Descreva a realidade cultural e territorial na Justificativa",
        })

    if re.search(r"(maior índice|maior taxa|único espaço|ausência total|nenhum equipamento)", diag, re.I):
        findings.append({
            "level": "medio",
            "category": "territorio",
            "location": "DIAGNOSTICO_TERRITORIAL",
            "problem": "Afirmações territoriais fortes sem fonte identificada",
            "impact": "Banca pode questionar a veracidade e descontar pontos",
            "suggestion": "Cite fonte ou reformule como: 'conforme percepção da equipe' ou 'segundo relato de moradores'",
        })

    return {
        "checklist": checklist,
        "findings": findings,
        "diagnostico_existe": len(diag) > 100,
    }
