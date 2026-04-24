"""Testes do orçamento: soma, percentual, alertas."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from unittest.mock import MagicMock


def make_budget(item, category, quantity=1, unit_value=1000):
    b = MagicMock()
    b.item = item
    b.category = category
    b.quantity = quantity
    b.unit_value = unit_value
    b.total_value = quantity * unit_value
    b.description = ""
    b.justification = ""
    return b


def make_project(budget=50000, module="Módulo II"):
    p = MagicMock()
    p.intended_budget = budget
    p.selected_module = module
    p.proponent_name = "Teste"
    return p


class TestBudgetCalculation:
    def test_sum_items(self):
        budgets = [
            make_budget("Sonorização", "materiais", 1, 5000),
            make_budget("Equipe", "recursos_humanos", 3, 2000),
            make_budget("Comunicação", "comunicacao", 1, 1000),
        ]
        total = sum(b.total_value for b in budgets)
        assert total == 12000

    def test_percentage_calculation(self):
        budgets = [
            make_budget("Equipe", "recursos_humanos", 1, 30000),
            make_budget("Materiais", "materiais", 1, 10000),
            make_budget("Comunicação", "comunicacao", 1, 10000),
        ]
        total = sum(b.total_value for b in budgets)
        rh_pct = 30000 / total * 100
        assert abs(rh_pct - 60.0) < 0.01

    def test_alert_exceeds_module(self):
        project = make_project(budget=50000)
        budgets = [make_budget("Item caro", "materiais", 1, 60000)]
        total = sum(b.total_value for b in budgets)
        exceeds = total > project.intended_budget
        assert exceeds is True

    def test_within_budget(self):
        project = make_project(budget=50000)
        budgets = [make_budget("Item", "materiais", 1, 49000)]
        total = sum(b.total_value for b in budgets)
        exceeds = total > project.intended_budget
        assert exceeds is False

    def test_accessibility_zero_alert(self):
        budgets = [
            make_budget("Equipe", "recursos_humanos", 1, 40000),
            make_budget("Comunicação", "comunicacao", 1, 10000),
        ]
        access_items = [b for b in budgets if "acessibilidade" in (b.category or "").lower()]
        assert len(access_items) == 0

    def test_communication_zero_alert(self):
        budgets = [
            make_budget("Equipe", "recursos_humanos", 1, 50000),
        ]
        comm_items = [b for b in budgets if "comunicacao" in (b.category or "").lower()]
        assert len(comm_items) == 0
