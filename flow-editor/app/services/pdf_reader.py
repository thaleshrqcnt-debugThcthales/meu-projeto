"""
Extrator de texto de PDFs usando pdfplumber (principal) e pypdf (fallback).
"""
from pathlib import Path
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_path: str | Path) -> Tuple[str, int, str]:
    """
    Retorna (texto_extraido, num_paginas, status).
    Status: 'ok' | 'parcial' | 'ilegivel'
    """
    path = Path(file_path)
    if not path.exists():
        return "", 0, "arquivo_nao_encontrado"

    text, page_count, status = _try_pdfplumber(path)

    if not text or len(text.strip()) < 100:
        text_fallback, page_count_fallback, status_fallback = _try_pypdf(path)
        if len(text_fallback.strip()) > len(text.strip()):
            return text_fallback, page_count_fallback, status_fallback

    return text, page_count, status


def _try_pdfplumber(path: Path) -> Tuple[str, int, str]:
    try:
        import pdfplumber
        pages_text = []
        with pdfplumber.open(str(path)) as pdf:
            page_count = len(pdf.pages)
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    pages_text.append(t)

        full_text = "\n\n".join(pages_text)
        if len(full_text.strip()) < 50:
            return full_text, page_count, "ilegivel"
        status = "parcial" if len(pages_text) < page_count else "ok"
        return full_text, page_count, status
    except Exception as e:
        logger.warning(f"pdfplumber falhou: {e}")
        return "", 0, "erro"


def _try_pypdf(path: Path) -> Tuple[str, int, str]:
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        page_count = len(reader.pages)
        pages_text = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                pages_text.append(t)

        full_text = "\n\n".join(pages_text)
        if len(full_text.strip()) < 50:
            return full_text, page_count, "ilegivel"
        status = "parcial" if len(pages_text) < page_count else "ok"
        return full_text, page_count, status
    except Exception as e:
        logger.warning(f"pypdf falhou: {e}")
        return "", 0, "erro"


def get_relevant_excerpts(text: str, keywords: list[str], context_chars: int = 300) -> list[str]:
    """Extrai trechos relevantes ao redor de palavras-chave."""
    excerpts = []
    text_lower = text.lower()
    for kw in keywords:
        idx = text_lower.find(kw.lower())
        if idx >= 0:
            start = max(0, idx - context_chars)
            end = min(len(text), idx + len(kw) + context_chars)
            excerpt = text[start:end].strip()
            if excerpt not in excerpts:
                excerpts.append(excerpt)
    return excerpts[:10]
