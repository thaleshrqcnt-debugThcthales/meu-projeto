"""
Auditoria determinística de coerência documental.
Não depende de IA — executa verificações por código puro.
"""
import re
from typing import Any
from dataclasses import dataclass, field


AI_MARKERS = [
    "como modelo de linguagem",
    "texto gerado",
    "versão adaptada",
    "conforme solicitado",
    "este projeto foi elaborado",
    "melhorias aplicadas",
    "ajustei",
    "rascunho",
    "placeholder",
    "lorem ipsum",
    "[inserir",
    "[preencher",
    "xxx",
    "como ia",
    "inteligência artificial gerou",
    "gerado por ia",
    "gerado automaticamente",
]

UNCONFIRMED_MARKERS = [
    "parceiro desejado",
    "espaço desejado",
    "em negociação",
    "a confirmar",
]


@dataclass
class Finding:
    level: str  # critico | medio | leve | sugestao
    category: str
    location: str
    problem: str
    impact: str
    suggestion: str

    def to_dict(self) -> dict:
        return {
            "level": self.level,
            "category": self.category,
            "location": self.location,
            "problem": self.problem,
            "impact": self.impact,
            "suggestion": self.suggestion,
        }


def _all_sections_text(sections: list) -> str:
    return "\n\n".join(s.content or "" for s in sections if s.content)


def _section_text(sections: list, name: str) -> str:
    for s in sections:
        if s.section_name == name:
            return s.content or ""
    return ""


def check_budget_total(project, budgets: list) -> list[Finding]:
    findings = []
    if not budgets:
        return findings

    total = sum(b.total_value for b in budgets)
    intended = project.intended_budget or 0

    if intended > 0 and total > 0:
        diff_pct = abs(total - intended) / intended
        if diff_pct > 0.05:  # mais de 5% de diferença
            level = "critico" if diff_pct > 0.10 else "medio"
            findings.append(Finding(
                level=level,
                category="orcamento",
                location="Orçamento",
                problem=f"Soma dos itens (R$ {total:,.2f}) difere do valor pretendido (R$ {intended:,.2f})",
                impact="Inconsistência orçamentária pode levar a desclassificação ou perda de nota",
                suggestion=f"Ajuste os itens para que a soma seja R$ {intended:,.2f} ou revise o valor pretendido",
            ))

    return findings


def check_accessibility_budget(budgets: list, sections: list) -> list[Finding]:
    findings = []
    access_section = _section_text(sections, "PLANO_ACESSIBILIDADE")
    if not access_section:
        return findings

    access_items = [b for b in budgets if "acessibilidade" in (b.category or "").lower()
                    or "libras" in (b.item or "").lower()
                    or "audiodescri" in (b.item or "").lower()]

    has_access_budget = any(b.total_value > 0 for b in access_items)

    if "libras" in access_section.lower() and not any(
        "libras" in (b.item or "").lower() for b in budgets
    ):
        findings.append(Finding(
            level="critico",
            category="acessibilidade",
            location="Plano de Acessibilidade / Orçamento",
            problem="Plano de Acessibilidade menciona Libras, mas não há rubrica de Libras no orçamento",
            impact="Compromisso sem recursos: risco de questionamento pela banca",
            suggestion="Adicione rubrica 'Intérprete de Libras' no orçamento com valor compatível",
        ))

    if "audiodescri" in access_section.lower() and not any(
        "audiodescri" in (b.item or "").lower() for b in budgets
    ):
        findings.append(Finding(
            level="critico",
            category="acessibilidade",
            location="Plano de Acessibilidade / Orçamento",
            problem="Plano menciona audiodescrição, mas não há rubrica correspondente no orçamento",
            impact="Promessa sem orçamento reduz credibilidade do plano de acessibilidade",
            suggestion="Adicione rubrica de audiodescrição no orçamento",
        ))

    if access_section and not has_access_budget and not access_items:
        findings.append(Finding(
            level="medio",
            category="acessibilidade",
            location="Orçamento",
            problem="Plano de Acessibilidade existe, mas nenhuma rubrica orçamentária está relacionada a acessibilidade",
            impact="Banca pode questionar a viabilidade real do plano",
            suggestion="Adicione ao menos uma rubrica de acessibilidade no orçamento (ex: mediação acessível, material em Braille, intérprete)",
        ))

    return findings


def check_communication_budget(budgets: list, sections: list) -> list[Finding]:
    findings = []
    comm_section = _section_text(sections, "PLANO_COMUNICACAO")
    if not comm_section:
        return findings

    comm_items = [b for b in budgets if "comunica" in (b.category or "").lower()
                  or "comunica" in (b.item or "").lower()
                  or "impulsionamento" in (b.item or "").lower()
                  or "assessoria" in (b.item or "").lower()]

    if comm_section and not comm_items:
        findings.append(Finding(
            level="medio",
            category="comunicacao",
            location="Plano de Comunicação / Orçamento",
            problem="Plano de Comunicação existe, mas não há rubrica de comunicação no orçamento",
            impact="Plano sem verba correspondente é inviável e pode ser questionado",
            suggestion="Adicione rubricas de comunicação (design, impulsionamento, impressão, etc.)",
        ))

    return findings


def check_title_consistency(project, sections: list) -> list[Finding]:
    findings = []
    title = project.public_title or project.internal_name or ""
    if not title:
        return findings

    all_text = _all_sections_text(sections)
    # Verifica se título aparece pelo menos no resumo e apresentação
    resumo = _section_text(sections, "RESUMO")
    apresentacao = _section_text(sections, "APRESENTACAO")

    title_short = title[:20].lower()
    if resumo and title_short not in resumo.lower() and title_short not in apresentacao.lower():
        findings.append(Finding(
            level="leve",
            category="identidade",
            location="RESUMO / APRESENTACAO",
            problem=f"Título '{title}' não aparece explicitamente no Resumo ou Apresentação",
            impact="Pode dificultar identificação do projeto pela banca",
            suggestion="Mencione o título completo do projeto no início do Resumo",
        ))

    return findings


def check_proponent_consistency(project, sections: list) -> list[Finding]:
    findings = []
    name = project.proponent_name or ""
    if not name:
        return findings

    all_text = _all_sections_text(sections)
    name_lower = name.lower()
    first_name = name.split()[0].lower() if name.split() else ""

    if first_name and first_name not in all_text.lower():
        findings.append(Finding(
            level="leve",
            category="identidade",
            location="Seções do projeto",
            problem=f"Nome do proponente '{name}' não aparece nas seções do projeto",
            impact="Banca pode não identificar o responsável pelo projeto",
            suggestion="Mencione o nome do proponente na Apresentação e na seção de Equipe",
        ))

    return findings


def check_module_mentions(project, sections: list) -> list[Finding]:
    findings = []
    module = project.selected_module or ""
    budget = project.intended_budget or 0

    if not module and not budget:
        return findings

    all_text = _all_sections_text(sections)

    if budget > 0:
        budget_str = f"{budget:,.0f}".replace(",", ".")
        wrong_values = []
        # Procura por outros valores monetários que não batem com o total
        import re
        money_matches = re.findall(r"R\$\s*[\d.,]+", all_text)
        for match in money_matches:
            val_str = re.sub(r"[R\$\s.]", "", match).replace(",", ".")
            try:
                val = float(val_str)
                if abs(val - budget) > budget * 0.1 and val > budget * 0.5:
                    wrong_values.append(match)
            except (ValueError, ZeroDivisionError):
                pass

        if wrong_values:
            findings.append(Finding(
                level="medio",
                category="valor",
                location="Seções do projeto",
                problem=f"Valores monetários divergentes encontrados: {', '.join(set(wrong_values[:3]))}",
                impact="Inconsistência de valores pode gerar dúvidas na banca sobre o módulo real",
                suggestion=f"Verifique se todos os valores no texto correspondem ao módulo de R$ {budget:,.2f}",
            ))

    return findings


def check_dates_consistency(sections: list, duration_months: int = None) -> list[Finding]:
    findings = []
    cronograma = _section_text(sections, "CRONOGRAMA")
    if not cronograma:
        return findings

    # Verifica se comunicação aparece antes de execução no cronograma
    lines = cronograma.lower().split("\n")
    comunicacao_line = None
    execucao_line = None

    for i, line in enumerate(lines):
        if "comunicação" in line or "divulgação" in line:
            comunicacao_line = i
        if "execução" in line or "realização" in line:
            execucao_line = i

    if comunicacao_line and execucao_line and comunicacao_line > execucao_line:
        findings.append(Finding(
            level="medio",
            category="cronograma",
            location="Cronograma",
            problem="Comunicação/divulgação aparece após execução no cronograma",
            impact="Cronograma logicamente incoerente: divulgação deve anteceder as ações",
            suggestion="Mova a fase de comunicação para antes da execução das ações principais",
        ))

    return findings


def check_required_sections(sections: list) -> list[Finding]:
    findings = []
    from app.services.project_generator import SECTION_NAMES

    existing = {s.section_name for s in sections if s.content and len(s.content.strip()) > 50}
    critical_sections = [
        "RESUMO", "JUSTIFICATIVA", "METODOLOGIA", "PUBLICO_ALVO",
        "PLANO_ACESSIBILIDADE", "CONTRAPARTIDA", "INDICADORES"
    ]

    for sec in critical_sections:
        if sec not in existing:
            findings.append(Finding(
                level="critico",
                category="completude",
                location=sec,
                problem=f"Seção '{sec}' está ausente ou vazia",
                impact="Seção obrigatória faltando pode causar desclassificação",
                suggestion=f"Gere ou preencha manualmente a seção '{sec}'",
            ))

    return findings


def check_for_ai_markers(sections: list) -> list[Finding]:
    findings = []
    all_text = _all_sections_text(sections).lower()

    for marker in AI_MARKERS:
        if marker.lower() in all_text:
            findings.append(Finding(
                level="critico",
                category="linguagem",
                location="Texto do projeto",
                problem=f"Marcador proibido encontrado: '{marker}'",
                impact="Marca de IA no texto compromete credibilidade perante a banca",
                suggestion=f"Remova toda ocorrência de '{marker}' e reescreva o trecho",
            ))

    return findings


def check_public_sum(sections: list) -> list[Finding]:
    findings = []
    metas = _section_text(sections, "METAS")
    acoes = _section_text(sections, "ACOES_PREVISTAS")
    resumo = _section_text(sections, "RESUMO")

    if not metas or not resumo:
        return findings

    import re
    # Extrai números de público do resumo e metas
    resumo_numbers = re.findall(r"(\d[\d.]*)\s*(?:pessoas|participantes|beneficiários)", resumo.lower())
    metas_numbers = re.findall(r"(\d[\d.]*)\s*(?:pessoas|participantes|beneficiários)", metas.lower())

    if resumo_numbers and metas_numbers:
        try:
            resumo_total = max(int(n.replace(".", "")) for n in resumo_numbers)
            metas_total = sum(int(n.replace(".", "")) for n in metas_numbers)
            if resumo_total > 0 and metas_total > 0 and abs(resumo_total - metas_total) > resumo_total * 0.2:
                findings.append(Finding(
                    level="critico",
                    category="publico",
                    location="Resumo / Metas",
                    problem=f"Público no Resumo ({resumo_total}) diverge das Metas ({metas_total})",
                    impact="Inconsistência de público é facilmente identificada pela banca",
                    suggestion="Alinhe os números de público-alvo entre Resumo e Metas",
                ))
        except (ValueError, TypeError):
            pass

    return findings


def check_team_budget_alignment(sections: list, budgets: list) -> list[Finding]:
    findings = []
    equipe = _section_text(sections, "EQUIPE")
    if not equipe or not budgets:
        return findings

    # Funções que devem estar no orçamento se aparecem na equipe
    critical_roles = {
        "produção": ["produção", "produtor"],
        "comunicação": ["comunicação", "assessoria"],
        "acessibilidade": ["acessibilidade", "libras", "mediador"],
        "registro": ["registro", "fotografia", "audiovisual", "filmagem"],
        "coordenação": ["coordenação", "coordenador", "direção"],
    }

    budget_text = " ".join(
        (b.item or "") + " " + (b.description or "") for b in budgets
    ).lower()

    for role, keywords in critical_roles.items():
        role_in_equipe = any(kw in equipe.lower() for kw in keywords)
        role_in_budget = any(kw in budget_text for kw in keywords)

        if role_in_equipe and not role_in_budget:
            findings.append(Finding(
                level="medio",
                category="equipe",
                location="Equipe / Orçamento",
                problem=f"Função '{role}' aparece na Equipe mas não tem rubrica no orçamento",
                impact="Equipe sem remuneração orçada gera questionamentos sobre viabilidade",
                suggestion=f"Adicione rubrica orçamentária para o profissional de {role}",
            ))

    return findings


def run_full_audit(project, sections: list, budgets: list) -> dict:
    """Executa todas as auditorias determinísticas e retorna resultado consolidado."""
    findings = []

    findings.extend(check_budget_total(project, budgets))
    findings.extend(check_accessibility_budget(budgets, sections))
    findings.extend(check_communication_budget(budgets, sections))
    findings.extend(check_title_consistency(project, sections))
    findings.extend(check_proponent_consistency(project, sections))
    findings.extend(check_module_mentions(project, sections))
    findings.extend(check_dates_consistency(sections, project.duration_months))
    findings.extend(check_required_sections(sections))
    findings.extend(check_for_ai_markers(sections))
    findings.extend(check_public_sum(sections))
    findings.extend(check_team_budget_alignment(sections, budgets))

    criticos = [f for f in findings if f.level == "critico"]
    medios = [f for f in findings if f.level == "medio"]
    leves = [f for f in findings if f.level == "leve"]

    # Score determinístico (complementa IA)
    base_score = 100
    base_score -= len(criticos) * 15
    base_score -= len(medios) * 5
    base_score -= len(leves) * 2
    score = max(0, min(100, base_score))

    if criticos:
        status = "ALTO RISCO DOCUMENTAL"
    elif len(medios) >= 4:
        status = "REVISAR ANTES DE ENVIAR"
    elif medios or leves:
        status = "APTO COM RESSALVAS"
    else:
        status = "APTO PARA EXPORTAR"

    return {
        "score": score,
        "status": status,
        "findings": [f.to_dict() for f in findings],
        "summary": f"{len(criticos)} críticos, {len(medios)} médios, {len(leves)} leves",
        "source": "deterministic",
    }
