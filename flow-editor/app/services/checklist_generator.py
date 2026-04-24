"""
Gera checklist documental a partir do edital extraído.
"""
import json
from app.services.ai_provider import ai_provider, load_prompt


def generate_checklist(edital_json: dict, proponent_type: str, selected_module: str) -> dict:
    """Gera checklist via IA a partir do edital."""
    prompt_template = load_prompt("gerar_checklist.md")

    prompt = (
        prompt_template
        .replace("{edital_json}", json.dumps(edital_json or {}, ensure_ascii=False, indent=2))
        .replace("{proponent_type}", proponent_type or "não informado")
        .replace("{selected_module}", selected_module or "não informado")
    )

    try:
        return ai_provider.complete_json(prompt, max_tokens=4000)
    except Exception as e:
        return {
            "checklist": _fallback_checklist(edital_json),
            "tarefas_preparacao": [],
            "alertas": [f"Erro na geração automática: {e}. Checklist básico gerado."],
        }


def _fallback_checklist(edital_json: dict) -> list:
    """Checklist básico baseado nos campos do edital."""
    checklist = []
    docs_obrigatorios = edital_json.get("documentos_obrigatorios", [])
    docs_condicionais = edital_json.get("documentos_condicionais", [])

    for doc in docs_obrigatorios:
        checklist.append({
            "documento": str(doc),
            "tipo": "obrigatorio",
            "condicao": "",
            "quem_apresenta": "proponente",
            "formato": "PDF",
            "prazo": "na inscrição",
            "status": "nao_iniciado",
            "observacao": "",
            "risco_se_faltar": "desclassificacao",
        })

    for doc in docs_condicionais:
        checklist.append({
            "documento": str(doc),
            "tipo": "condicional",
            "condicao": "verificar no edital",
            "quem_apresenta": "proponente",
            "formato": "PDF",
            "prazo": "na inscrição",
            "status": "nao_iniciado",
            "observacao": "",
            "risco_se_faltar": "perda_de_nota",
        })

    if not checklist:
        checklist = [
            {
                "documento": "Formulário de inscrição",
                "tipo": "obrigatorio",
                "condicao": "",
                "quem_apresenta": "proponente",
                "formato": "PDF/plataforma online",
                "prazo": "data limite do edital",
                "status": "nao_iniciado",
                "observacao": "Verificar no edital qual plataforma",
                "risco_se_faltar": "desclassificacao",
            },
            {
                "documento": "Documentação pessoal (CPF/RG ou CNPJ)",
                "tipo": "obrigatorio",
                "condicao": "",
                "quem_apresenta": "proponente",
                "formato": "PDF",
                "prazo": "na inscrição",
                "status": "nao_iniciado",
                "observacao": "",
                "risco_se_faltar": "desclassificacao",
            },
            {
                "documento": "Projeto cultural",
                "tipo": "obrigatorio",
                "condicao": "",
                "quem_apresenta": "proponente",
                "formato": "DOCX/PDF",
                "prazo": "na inscrição",
                "status": "nao_iniciado",
                "observacao": "",
                "risco_se_faltar": "desclassificacao",
            },
            {
                "documento": "Planilha orçamentária",
                "tipo": "obrigatorio",
                "condicao": "",
                "quem_apresenta": "proponente",
                "formato": "XLSX/PDF",
                "prazo": "na inscrição",
                "status": "nao_iniciado",
                "observacao": "",
                "risco_se_faltar": "desclassificacao",
            },
        ]

    return checklist
