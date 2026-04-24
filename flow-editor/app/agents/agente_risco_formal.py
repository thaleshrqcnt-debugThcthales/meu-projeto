"""
Agente Risco Formal: detecta riscos de desclassificação e perda de nota.
"""


def detectar_riscos(project, sections: list, budgets: list, edital_json: dict) -> dict:
    riscos = []

    # Valor vs módulo
    if project.intended_budget and edital_json:
        for mod in edital_json.get("modulos", []):
            mod_nome = str(mod.get("nome", "")).lower()
            mod_valor_str = str(mod.get("valor", "")).replace("R$", "").replace(".", "").replace(",", ".").strip()
            try:
                mod_valor = float(mod_valor_str)
                if mod_nome in (project.selected_module or "").lower():
                    if project.intended_budget > mod_valor * 1.01:
                        riscos.append({
                            "nivel": "critico",
                            "tipo": "valor_excedido",
                            "descricao": f"Valor pretendido (R$ {project.intended_budget:,.2f}) excede o limite do módulo (R$ {mod_valor:,.2f})",
                            "consequencia": "Desclassificação automática",
                            "acao": "Reduza o orçamento ou revise o módulo escolhido",
                        })
            except (ValueError, TypeError):
                pass

    # Seções críticas ausentes
    section_names = {s.section_name for s in sections if s.content and len(s.content.strip()) > 50}
    for sec in ["RESUMO", "METODOLOGIA", "PUBLICO_ALVO", "PLANO_ACESSIBILIDADE"]:
        if sec not in section_names:
            riscos.append({
                "nivel": "critico",
                "tipo": "secao_ausente",
                "descricao": f"Seção '{sec}' ausente ou vazia",
                "consequencia": "Possível desclassificação ou perda significativa de pontos",
                "acao": f"Gere ou preencha a seção '{sec}' antes de exportar",
            })

    # Orçamento vazio
    if not budgets:
        riscos.append({
            "nivel": "critico",
            "tipo": "orcamento_vazio",
            "descricao": "Orçamento não preenchido",
            "consequencia": "Projeto sem viabilidade financeira demonstrada",
            "acao": "Preencha o orçamento com todos os itens necessários",
        })

    # Contrapartida ausente
    contrapartida = next((s for s in sections if s.section_name == "CONTRAPARTIDA"), None)
    if edital_json and edital_json.get("exigencias_contrapartida"):
        if not contrapartida or not contrapartida.content or len(contrapartida.content.strip()) < 50:
            riscos.append({
                "nivel": "critico",
                "tipo": "contrapartida_ausente",
                "descricao": "Edital exige contrapartida, mas a seção está vazia",
                "consequencia": "Desclassificação ou perda de pontos em critério específico",
                "acao": "Preencha a seção de Contrapartida",
            })

    criticos = [r for r in riscos if r["nivel"] == "critico"]
    medios = [r for r in riscos if r["nivel"] == "medio"]

    return {
        "riscos": riscos,
        "total_criticos": len(criticos),
        "total_medios": len(medios),
        "status": "ALTO RISCO" if criticos else ("ATENÇÃO" if medios else "OK"),
    }
