"""
Simula parecer de banca avaliadora de edital cultural.
"""
import json
from app.services.ai_provider import ai_provider, load_prompt

COMPETITIVE_RANGES = {
    (0, 40): ("frágil", "O projeto apresenta fragilidades estruturais significativas que comprometem sua competitividade."),
    (41, 60): ("mediano", "O projeto atende requisitos básicos, mas precisa de fortalecimento em aspectos centrais."),
    (61, 75): ("bom, mas com risco", "O projeto tem qualidade, mas apresenta vulnerabilidades que podem custar pontos na avaliação."),
    (76, 85): ("competitivo", "O projeto tem potencial competitivo real, desde que a documentação esteja completa."),
    (86, 92): ("muito competitivo", "O projeto apresenta alto potencial. Pequenos ajustes podem maximizar a nota."),
    (93, 100): ("alto potencial", "O projeto tem alto potencial de avaliação positiva, condicionado à documentação correta."),
}


def get_competitive_range(score: float) -> tuple[str, str]:
    for (low, high), (label, desc) in COMPETITIVE_RANGES.items():
        if low <= score <= high:
            return label, desc
    return "indefinido", ""


def simulate_score(project, sections: list, budgets: list, schedules: list, edital_json: dict) -> dict:
    """Simula parecer de banca via IA."""
    prompt_template = load_prompt("simular_banca.md")

    # Monta dados do projeto
    sections_summary = "\n\n".join(
        f"## {s.section_name}\n{(s.content or '')[:800]}"
        for s in sections if s.content
    )

    budget_summary = "\n".join(
        f"- {b.item}: {b.quantity} x R$ {b.unit_value:.2f} = R$ {b.total_value:.2f}"
        for b in budgets
    ) or "Orçamento não preenchido"

    schedule_summary = "\n".join(
        f"- {s.phase} | {s.month}: {s.activity}"
        for s in schedules
    ) or "Cronograma não preenchido"

    project_data = f"""
Nome: {project.public_title or project.internal_name}
Proponente: {project.proponent_name}
Módulo: {project.selected_module}
Valor pretendido: R$ {project.intended_budget or 0:,.2f}
Duração: {project.duration_months} meses
Linguagem: {project.cultural_language}
Modalidade: {project.modality}

{sections_summary}
"""

    prompt = (
        prompt_template
        .replace("{project_data}", project_data)
        .replace("{edital_json}", json.dumps(edital_json or {}, ensure_ascii=False, indent=2))
        .replace("{budget_data}", budget_summary)
        .replace("{schedule_data}", schedule_summary)
    )

    try:
        result = ai_provider.complete_json(prompt, max_tokens=6000)
        total = result.get("total_score", 0)
        range_label, _ = get_competitive_range(total)
        result["competitive_range"] = result.get("competitive_range", range_label)
        result.setdefault("disclaimer",
            "Esta simulação tem finalidade técnica de preparação. "
            "A aprovação real depende da banca, concorrência e critérios definitivos do edital."
        )
        return result
    except Exception as e:
        return {
            "c1_score": 0, "c2_score": 0, "c3_score": 0, "c4_score": 0, "c5_score": 0,
            "total_score": 0,
            "competitive_range": "erro na simulação",
            "opinion_text": f"Erro ao simular: {e}",
            "recommendations": ["Verifique a API key e tente novamente"],
            "criteria_details": [],
            "disclaimer": "Simulação não concluída por erro técnico.",
        }
