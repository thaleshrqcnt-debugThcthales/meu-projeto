"""
Gera seções completas do projeto cultural usando IA.
"""
from typing import Optional
from app.services.ai_provider import ai_provider, load_prompt

SECTION_NAMES = [
    "TITULO", "RESUMO", "APRESENTACAO", "JUSTIFICATIVA",
    "DIAGNOSTICO_TERRITORIAL", "OBJETIVO_GERAL", "OBJETIVOS_ESPECIFICOS",
    "PUBLICO_ALVO", "METAS", "METODOLOGIA", "ACOES_PREVISTAS",
    "CRONOGRAMA", "EQUIPE", "PLANO_ACESSIBILIDADE", "PLANO_COMUNICACAO",
    "CONTRAPARTIDA", "INDICADORES", "ORCAMENTO_NARRATIVO",
    "RISCOS_MITIGACAO", "RESULTADOS_ESPERADOS", "LEGADO",
    "CHECKLIST_ANEXOS", "ADEQUACAO_EDITAL",
]

SECTION_LABELS = {
    "TITULO": "Título",
    "RESUMO": "Resumo",
    "APRESENTACAO": "Apresentação",
    "JUSTIFICATIVA": "Justificativa",
    "DIAGNOSTICO_TERRITORIAL": "Diagnóstico Cultural e Territorial",
    "OBJETIVO_GERAL": "Objetivo Geral",
    "OBJETIVOS_ESPECIFICOS": "Objetivos Específicos",
    "PUBLICO_ALVO": "Público-Alvo",
    "METAS": "Metas",
    "METODOLOGIA": "Metodologia",
    "ACOES_PREVISTAS": "Ações Previstas",
    "CRONOGRAMA": "Cronograma",
    "EQUIPE": "Equipe",
    "PLANO_ACESSIBILIDADE": "Plano de Acessibilidade",
    "PLANO_COMUNICACAO": "Plano de Comunicação",
    "CONTRAPARTIDA": "Contrapartida Social/Cultural",
    "INDICADORES": "Indicadores de Avaliação",
    "ORCAMENTO_NARRATIVO": "Orçamento (Narrativa)",
    "RISCOS_MITIGACAO": "Riscos e Mitigação",
    "RESULTADOS_ESPERADOS": "Resultados Esperados",
    "LEGADO": "Legado",
    "CHECKLIST_ANEXOS": "Checklist de Anexos",
    "ADEQUACAO_EDITAL": "Adequação ao Edital",
}


def build_prompt(project, briefing, edital_json: dict) -> str:
    template = load_prompt("gerar_projeto.md")

    import json as json_mod
    edital_str = json_mod.dumps(edital_json, ensure_ascii=False, indent=2) if edital_json else "{}"

    replacements = {
        "{edital_json}": edital_str,
        "{proponent_name}": project.proponent_name or "não informado",
        "{proponent_type}": project.proponent_type or "não informado",
        "{city}": project.city or "não informado",
        "{state}": project.state or "não informado",
        "{cultural_language}": project.cultural_language or "não informado",
        "{modality}": project.modality or "não informado",
        "{selected_module}": project.selected_module or "não informado",
        "{intended_budget}": str(project.intended_budget or "não informado"),
        "{duration_months}": str(project.duration_months or "não informado"),
        "{briefing_free_text}": (briefing.free_text if briefing else "") or "não informado",
        "{territory}": (briefing.territory if briefing else "") or "não informado",
        "{target_audience}": (briefing.target_audience if briefing else "") or "não informado",
        "{team_artists}": (briefing.team_artists if briefing else "") or "não informado",
        "{planned_actions}": (briefing.planned_actions if briefing else "") or "não informado",
        "{desired_spaces}": (briefing.desired_spaces if briefing else "") or "não informado",
        "{cultural_references}": (briefing.cultural_references if briefing else "") or "não informado",
        "{confirmed_partners}": (briefing.confirmed_partners if briefing else "") or "nenhum confirmado",
        "{desired_partners}": (briefing.desired_partners if briefing else "") or "nenhum indicado",
        "{proponent_history}": (briefing.proponent_history if briefing else "") or "não informado",
        "{needed_materials}": (briefing.needed_materials if briefing else "") or "não informado",
        "{desired_accessibility}": (briefing.desired_accessibility if briefing else "") or "não informado",
        "{desired_counterpart}": (briefing.desired_counterpart if briefing else "") or "não informado",
    }

    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)

    return template


def parse_sections(raw_text: str) -> dict[str, str]:
    """Divide o texto gerado nas seções marcadas com ###."""
    import re
    sections = {}
    pattern = r"###\s*\[?([A-Z_]+)\]?\s*\n([\s\S]*?)(?=###\s*\[?[A-Z_]+\]?|$)"
    matches = re.findall(pattern, raw_text)
    for name, content in matches:
        name = name.strip()
        if name in SECTION_NAMES:
            sections[name] = content.strip()
    return sections


def generate_project(project, briefing, edital_json: dict) -> dict[str, str]:
    """Gera todas as seções do projeto. Retorna dict {section_name: content}."""
    prompt = build_prompt(project, briefing, edital_json)
    raw = ai_provider.complete(prompt, max_tokens=12000)
    sections = parse_sections(raw)

    # Garante que todas as seções existam (mesmo que vazias)
    for name in SECTION_NAMES:
        if name not in sections:
            sections[name] = ""

    return sections


def generate_single_section(project, briefing, edital_json: dict, section_name: str) -> str:
    """Regenera uma seção específica."""
    prompt = build_prompt(project, briefing, edital_json)
    prompt += f"\n\nGere APENAS a seção [{section_name}] completa."
    raw = ai_provider.complete(prompt, max_tokens=4000)
    sections = parse_sections(raw)
    return sections.get(section_name, raw.strip())
