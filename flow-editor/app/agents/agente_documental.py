"""
Agente Documental: checa documentos e anexos necessários.
"""
from app.services.checklist_generator import generate_checklist


def gerar_checklist(project, edital_json: dict) -> dict:
    return generate_checklist(edital_json, project.proponent_type, project.selected_module)
