"""Testes do exportador DOCX."""
import sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from unittest.mock import MagicMock
from pathlib import Path


def make_project():
    p = MagicMock()
    p.id = 1
    p.internal_name = "festival-teste"
    p.public_title = "Festival Cultural de Teste"
    p.proponent_name = "Maria Artista"
    p.proponent_type = "pessoa_fisica"
    p.city = "São Paulo"
    p.state = "SP"
    p.cultural_language = "Música"
    p.modality = "Festival"
    p.selected_module = "Módulo I"
    p.intended_budget = 30000.0
    p.duration_months = 6
    return p


def make_section(name, content):
    s = MagicMock()
    s.section_name = name
    s.content = content
    return s


def make_budget_item(item, category, qty, unit_val):
    b = MagicMock()
    b.item = item
    b.category = category
    b.quantity = qty
    b.unit_value = unit_val
    b.total_value = qty * unit_val
    b.description = f"Descrição de {item}"
    b.justification = f"Justificativa de {item}"
    b.unit = "un"
    return b


def make_schedule(phase, month, activity, responsible):
    s = MagicMock()
    s.phase = phase
    s.month = month
    s.activity = activity
    s.responsible = responsible
    s.evidence = "Relatório"
    return s


class TestDocxExporter:
    def test_generates_file(self):
        from app.services.docx_exporter import export_project_docx

        project = make_project()
        sections = [
            make_section("RESUMO", "O projeto Festival Cultural de Teste realiza 3 shows no bairro central."),
            make_section("JUSTIFICATIVA", "A região carece de programação cultural regular."),
            make_section("METODOLOGIA", "As ações serão realizadas em três fins de semana."),
        ]
        budgets = [
            make_budget_item("Músicos", "recursos_humanos", 5, 1500),
            make_budget_item("Sonorização", "materiais", 1, 8000),
            make_budget_item("Comunicação", "comunicacao", 1, 2000),
        ]
        schedules = [
            make_schedule("Pré-produção", "Mês 1", "Contratar equipe", "Produtora"),
            make_schedule("Execução", "Mês 3", "Realização dos shows", "Direção Artística"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "projeto_teste.docx")
            result = export_project_docx(project, sections, budgets, schedules, output)
            assert Path(result).exists()
            assert Path(result).stat().st_size > 5000  # arquivo real, não vazio

    def test_file_has_content(self):
        from app.services.docx_exporter import export_project_docx
        from docx import Document

        project = make_project()
        sections = [make_section("RESUMO", "Texto de teste do projeto cultural.")]
        budgets = [make_budget_item("Item teste", "materiais", 1, 1000)]
        schedules = []

        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "test.docx")
            export_project_docx(project, sections, budgets, schedules, output)
            doc = Document(output)
            text = "\n".join(p.text for p in doc.paragraphs)
            assert "Festival Cultural de Teste" in text

    def test_audit_docx_generates(self):
        from app.services.docx_exporter import export_audit_docx

        project = make_project()
        audit_data = {
            "score": 75,
            "status": "APTO COM RESSALVAS",
            "summary": "2 críticos, 1 médio, 0 leves",
            "findings": [
                {
                    "level": "critico",
                    "category": "orcamento",
                    "location": "Orçamento",
                    "problem": "Soma incorreta",
                    "impact": "Risco de desclassificação",
                    "suggestion": "Ajuste os valores",
                }
            ],
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "auditoria.docx")
            result = export_audit_docx(audit_data, project, output)
            assert Path(result).exists()

    def test_score_docx_generates(self):
        from app.services.docx_exporter import export_score_docx

        project = make_project()
        score_data = {
            "c1_score": 16, "c2_score": 15, "c3_score": 14, "c4_score": 13, "c5_score": 12,
            "total_score": 70,
            "competitive_range": "bom, mas com risco",
            "opinion_text": "O projeto apresenta mérito cultural relevante.",
            "recommendations": ["Reforçar orçamento", "Detalhar metodologia"],
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "score.docx")
            result = export_score_docx(score_data, project, output)
            assert Path(result).exists()
