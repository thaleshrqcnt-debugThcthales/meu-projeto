"""Testes da auditoria determinística de coerência."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from unittest.mock import MagicMock
from app.services.consistency_auditor import (
    check_budget_total,
    check_for_ai_markers,
    check_accessibility_budget,
    check_communication_budget,
    check_title_consistency,
    run_full_audit,
)


def make_project(intended_budget=50000, title="Festival Teste", proponent="João Silva", module="Módulo II"):
    p = MagicMock()
    p.intended_budget = intended_budget
    p.public_title = title
    p.internal_name = title
    p.proponent_name = proponent
    p.selected_module = module
    p.duration_months = 6
    return p


def make_section(name, content):
    s = MagicMock()
    s.section_name = name
    s.content = content
    return s


def make_budget(item, category, quantity=1, unit_value=100, total_value=None):
    b = MagicMock()
    b.item = item
    b.category = category
    b.quantity = quantity
    b.unit_value = unit_value
    b.total_value = total_value if total_value is not None else quantity * unit_value
    b.description = ""
    b.justification = ""
    return b


class TestBudgetTotal:
    def test_correct_total(self):
        project = make_project(intended_budget=10000)
        budgets = [make_budget("Item A", "materiais", 1, 10000)]
        findings = check_budget_total(project, budgets)
        assert len(findings) == 0

    def test_divergent_total_critical(self):
        project = make_project(intended_budget=50000)
        budgets = [make_budget("Item A", "materiais", 1, 30000)]
        findings = check_budget_total(project, budgets)
        assert len(findings) == 1
        assert findings[0].level == "critico"

    def test_divergent_total_medium(self):
        project = make_project(intended_budget=50000)
        # 7% difference → medium
        budgets = [make_budget("Item A", "materiais", 1, 46500)]
        findings = check_budget_total(project, budgets)
        assert len(findings) == 1
        assert findings[0].level in ("medio", "critico")

    def test_empty_budget(self):
        project = make_project(intended_budget=50000)
        findings = check_budget_total(project, [])
        assert findings == []


class TestAIMarkers:
    def test_detects_ai_marker(self):
        sections = [make_section("RESUMO", "O projeto conforme solicitado foi elaborado para atender.")]
        findings = check_for_ai_markers(sections)
        assert any("conforme solicitado" in f.problem for f in findings)

    def test_detects_placeholder(self):
        sections = [make_section("METODOLOGIA", "A equipe [inserir nomes] realizará as ações.")]
        findings = check_for_ai_markers(sections)
        assert any("[inserir" in f.problem for f in findings)

    def test_clean_text(self):
        sections = [make_section("RESUMO", "O projeto realiza ações culturais no território da Zona Norte.")]
        findings = check_for_ai_markers(sections)
        assert len(findings) == 0


class TestAccessibilityBudget:
    def test_libras_in_plan_but_not_in_budget(self):
        sections = [make_section("PLANO_ACESSIBILIDADE", "O projeto contará com intérprete de Libras em todas as ações.")]
        budgets = [make_budget("Sonorização", "materiais")]
        findings = check_accessibility_budget(budgets, sections)
        assert any("Libras" in f.problem for f in findings)
        assert any(f.level == "critico" for f in findings)

    def test_libras_in_plan_and_budget(self):
        sections = [make_section("PLANO_ACESSIBILIDADE", "O projeto contará com intérprete de Libras.")]
        budgets = [make_budget("Intérprete de Libras", "acessibilidade")]
        findings = check_accessibility_budget(budgets, sections)
        assert not any("Libras" in f.problem for f in findings)

    def test_no_accessibility_plan(self):
        sections = [make_section("RESUMO", "Projeto cultural.")]
        budgets = []
        findings = check_accessibility_budget(budgets, sections)
        assert findings == []


class TestCommunicationBudget:
    def test_plan_without_budget(self):
        sections = [make_section("PLANO_COMUNICACAO", "O projeto terá impulsionamento em redes sociais e assessoria de imprensa.")]
        budgets = [make_budget("Sonorização", "materiais")]
        findings = check_communication_budget(budgets, sections)
        assert len(findings) > 0

    def test_plan_with_budget(self):
        sections = [make_section("PLANO_COMUNICACAO", "O projeto terá comunicação ampla.")]
        budgets = [make_budget("Assessoria de comunicação", "comunicacao")]
        findings = check_communication_budget(budgets, sections)
        assert len(findings) == 0


class TestRunFullAudit:
    def test_returns_score_and_status(self):
        project = make_project(intended_budget=50000)
        sections = [
            make_section("RESUMO", "Festival Teste apresenta ações culturais no território."),
            make_section("METODOLOGIA", "A metodologia envolve 3 ações presenciais."),
            make_section("PLANO_ACESSIBILIDADE", "O projeto oferece mediação acessível."),
            make_section("PLANO_COMUNICACAO", "Comunicação ampla via redes."),
        ]
        budgets = [
            make_budget("Produção", "recursos_humanos", 1, 50000),
        ]
        result = run_full_audit(project, sections, budgets)
        assert "score" in result
        assert "status" in result
        assert "findings" in result
        assert isinstance(result["score"], (int, float))
        assert 0 <= result["score"] <= 100

    def test_critical_issues_lower_score(self):
        project = make_project(intended_budget=50000)
        sections = [
            make_section("RESUMO", "Conforme solicitado, o projeto foi elaborado [inserir dados]."),
            make_section("PLANO_ACESSIBILIDADE", "O projeto terá intérprete de Libras e audiodescrição."),
        ]
        budgets = [make_budget("Item único", "materiais", 1, 20000)]  # diverge de 50000
        result = run_full_audit(project, sections, budgets)
        assert result["score"] < 80
        assert len(result["findings"]) > 0
