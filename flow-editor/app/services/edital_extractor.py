"""
Extrai informações estruturadas de editais culturais usando IA.
"""
import json
from typing import Optional
from app.services.ai_provider import ai_provider, load_prompt
from app.services.pdf_reader import extract_text_from_pdf

NOT_FOUND = "NÃO IDENTIFICADO AUTOMATICAMENTE — REVISAR MANUALMENTE"

EMPTY_STRUCTURE = {
    "nome_edital": NOT_FOUND,
    "orgao_responsavel": NOT_FOUND,
    "objeto": NOT_FOUND,
    "periodo_inscricao": NOT_FOUND,
    "quem_pode_participar": [],
    "quem_nao_pode_participar": [],
    "modulos": [],
    "criterios_avaliacao": [],
    "bonificacoes": [],
    "documentos_obrigatorios": [],
    "documentos_condicionais": [],
    "anexos": [],
    "regras_orcamento": [],
    "exigencias_acessibilidade": [],
    "exigencias_contrapartida": [],
    "exigencias_comunicacao": [],
    "prazos_execucao": [],
    "prestacao_contas": [],
    "riscos_formais": [],
    "campos_nao_identificados": [],
}

# Limite de caracteres enviados para IA (evita tokens desnecessários)
MAX_TEXT_FOR_AI = 80_000


def extract_edict(text: str) -> dict:
    """Extrai estrutura do edital a partir do texto completo."""
    if not text or len(text.strip()) < 100:
        structure = EMPTY_STRUCTURE.copy()
        structure["campos_nao_identificados"].append("Texto do edital vazio ou ilegível")
        return structure

    prompt_template = load_prompt("raio_x_edital.md")
    truncated_text = text[:MAX_TEXT_FOR_AI]
    prompt = prompt_template.replace("{edital_text}", truncated_text)

    try:
        result = ai_provider.complete_json(prompt)
        return _normalize_structure(result)
    except Exception as e:
        structure = EMPTY_STRUCTURE.copy()
        structure["campos_nao_identificados"].append(f"Erro na extração automática: {str(e)}")
        return structure


def extract_edict_from_pdf(file_path: str) -> tuple[dict, str, int, str]:
    """
    Extrai edital de arquivo PDF.
    Retorna (estrutura_json, texto_bruto, num_paginas, status).
    """
    text, page_count, status = extract_text_from_pdf(file_path)
    structure = extract_edict(text)
    return structure, text, page_count, status


def _normalize_structure(data: dict) -> dict:
    """Garante que todos os campos existam e listas sejam listas."""
    result = EMPTY_STRUCTURE.copy()
    for key in result:
        if key in data:
            val = data[key]
            if isinstance(result[key], list) and not isinstance(val, list):
                result[key] = [str(val)] if val else []
            elif isinstance(result[key], str) and not isinstance(val, str):
                result[key] = str(val) if val else NOT_FOUND
            else:
                result[key] = val
    return result
