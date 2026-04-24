"""
Agente Orçamentista: audita o orçamento do projeto.
"""
import json
from app.services.ai_provider import ai_provider, load_prompt


def auditar_orcamento(project, budgets: list, sections: list, edital_json: dict) -> dict:
    """Audita orçamento via IA."""
    prompt_template = load_prompt("auditar_orcamento.md")

    budget_items_str = "\n".join(
        f"- {b.item} | {b.category} | {b.unit} | {b.quantity} x R$ {b.unit_value:.2f} = R$ {b.total_value:.2f} | {b.justification or ''}"
        for b in budgets
    ) or "Orçamento vazio"

    project_summary = ""
    for s in sections:
        if s.section_name in ("RESUMO", "METODOLOGIA", "PLANO_ACESSIBILIDADE", "PLANO_COMUNICACAO"):
            project_summary += f"\n## {s.section_name}\n{(s.content or '')[:500]}\n"

    orcamento_rules = "\n".join(edital_json.get("regras_orcamento", [])) if edital_json else ""

    prompt = (
        prompt_template
        .replace("{intended_budget}", str(project.intended_budget or 0))
        .replace("{selected_module}", project.selected_module or "não informado")
        .replace("{budget_items}", budget_items_str)
        .replace("{project_summary}", project_summary)
        .replace("{orcamento_rules}", orcamento_rules or "Não identificado no edital")
    )

    try:
        return ai_provider.complete_json(prompt, max_tokens=4000)
    except Exception as e:
        total = sum(b.total_value for b in budgets)
        return {
            "total_orcado": total,
            "total_pretendido": project.intended_budget or 0,
            "diferenca": total - (project.intended_budget or 0),
            "status_soma": "ok" if abs(total - (project.intended_budget or 0)) < 1 else "divergente",
            "percentuais": {},
            "alertas": [{"nivel": "leve", "item": "geral", "problema": f"Erro na auditoria automática: {e}", "sugestao": "Revise manualmente"}],
            "itens_ausentes": [],
            "itens_questionaveis": [],
            "recomendacao": "Revise o orçamento manualmente",
        }
