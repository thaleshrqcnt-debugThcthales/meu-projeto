"""
Cria pacote ZIP final com todos os arquivos do projeto.
"""
import zipfile
from pathlib import Path
from datetime import datetime


def create_package_zip(
    project,
    docx_path: str = None,
    xlsx_path: str = None,
    audit_docx_path: str = None,
    score_docx_path: str = None,
    md_path: str = None,
    output_path: str = None,
) -> str:
    if not output_path:
        safe_name = "".join(c for c in (project.internal_name or "projeto") if c.isalnum() or c in " _-")[:40]
        output_path = str(Path("app/exports") / f"pacote_final_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(str(path), "w", compression=zipfile.ZIP_DEFLATED) as zf:
        files = [
            (docx_path, "projeto_completo.docx"),
            (xlsx_path, "orcamento.xlsx"),
            (audit_docx_path, "relatorio_auditoria.docx"),
            (score_docx_path, "parecer_banca_simulada.docx"),
            (md_path, "projeto_completo.md"),
        ]
        for file_path, arcname in files:
            if file_path and Path(file_path).exists():
                zf.write(file_path, arcname)

        # README dentro do ZIP
        readme_content = f"""PACOTE FINAL — {project.public_title or project.internal_name}
Proponente: {project.proponent_name}
Módulo: {project.selected_module or 'não definido'}
Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}

CONTEÚDO DO PACOTE:
- projeto_completo.docx: Projeto cultural completo para inscrição
- orcamento.xlsx: Planilha orçamentária detalhada
- relatorio_auditoria.docx: Relatório de auditoria de coerência
- parecer_banca_simulada.docx: Simulação de parecer de banca
- projeto_completo.md: Versão em Markdown do projeto

AVISO IMPORTANTE:
Este pacote foi gerado pelo FLOW EDITOR — Sistema Operacional de Projetos Culturais.
A geração por sistema não garante aprovação. A avaliação final depende da banca,
da concorrência específica, dos critérios do edital e da documentação complementar.

Revise todos os documentos antes de enviar sua inscrição.
"""
        zf.writestr("LEIA-ME.txt", readme_content)

    return str(path)


def export_project_md(project, sections: list, output_path: str) -> str:
    """Exporta projeto em Markdown."""
    from app.services.project_generator import SECTION_LABELS

    lines = [
        f"# {project.public_title or project.internal_name}",
        "",
        f"**Proponente:** {project.proponent_name}  ",
        f"**Módulo:** {project.selected_module or 'não definido'}  ",
        f"**Valor:** R$ {project.intended_budget:,.2f}" if project.intended_budget else "**Valor:** não definido",
        f"**Duração:** {project.duration_months} meses" if project.duration_months else "",
        "",
        "---",
        "",
    ]

    section_order = [
        "RESUMO", "APRESENTACAO", "JUSTIFICATIVA", "DIAGNOSTICO_TERRITORIAL",
        "OBJETIVO_GERAL", "OBJETIVOS_ESPECIFICOS", "PUBLICO_ALVO", "METAS",
        "METODOLOGIA", "ACOES_PREVISTAS", "CRONOGRAMA", "EQUIPE",
        "PLANO_ACESSIBILIDADE", "PLANO_COMUNICACAO", "CONTRAPARTIDA",
        "INDICADORES", "ORCAMENTO_NARRATIVO", "RISCOS_MITIGACAO",
        "RESULTADOS_ESPERADOS", "LEGADO", "CHECKLIST_ANEXOS", "ADEQUACAO_EDITAL",
    ]

    sections_dict = {s.section_name: s.content for s in sections if s.content}

    for sec_name in section_order:
        content = sections_dict.get(sec_name, "")
        label = SECTION_LABELS.get(sec_name, sec_name)
        lines.append(f"## {label}")
        lines.append("")
        if content:
            lines.append(content)
        else:
            lines.append("_Seção não preenchida_")
        lines.append("")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)
