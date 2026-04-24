"""
Agente Humanizer: reescreve trechos com linguagem cultural técnica.
"""
from app.services.humanizer import humanize


def reescrever(text: str, mode: str = "tecnico-cultural", section_context: str = "") -> str:
    return humanize(text, mode, section_context)
