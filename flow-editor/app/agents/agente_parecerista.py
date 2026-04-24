"""
Agente Parecerista: avalia o projeto como banca de edital cultural.
"""
import json
from app.services.ai_provider import ai_provider
from app.services.score_simulator import simulate_score, get_competitive_range


def avaliar(project, sections: list, budgets: list, schedules: list, edital_json: dict) -> dict:
    """Executa simulação completa de banca."""
    result = simulate_score(project, sections, budgets, schedules, edital_json)
    total = result.get("total_score", 0)
    label, desc = get_competitive_range(total)
    result["range_label"] = label
    result["range_description"] = desc
    return result
