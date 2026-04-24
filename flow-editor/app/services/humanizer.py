"""
Reescreve trechos do projeto com linguagem técnica cultural, sem marcas de IA.
"""
from app.services.ai_provider import ai_provider, load_prompt

MODE_INSTRUCTIONS = {
    "tecnico-cultural": "Priorize linguagem técnica de gestão cultural. Verbos concretos, ações verificáveis, sem frases de impacto vazio.",
    "banca-conservadora": "Escreva de forma sóbria, objetiva e formal. Evite excessos retóricos. Cada frase deve ser defensável tecnicamente.",
    "artistico-controlado": "Preserve identidade artística, mas mantenha rigor técnico. Sem manifesto excessivo.",
    "justificativa-territorial": "Foque em dados territoriais confirmados. Separe percepção de dado. Use: 'segundo relato do proponente', 'conforme observação da equipe'.",
    "metodologia-objetiva": "Descreva método, ferramenta, etapa, responsável, resultado esperado. Cada parágrafo = uma ação.",
    "acessibilidade": "Use linguagem técnica de acessibilidade cultural. Mencione: arquitetônica, comunicacional, atitudinal. Verbos concretos.",
    "orcamento": "Justifique rubricas com relação direta à metodologia. Seja objetivo, sem retórica.",
    "contrapartida": "Descreva ação pública com: o quê, onde, para quem, duração, acesso gratuito ou não, como comprovar.",
    "resumo-curto": "Máximo 300 palavras. Inclua: objeto, metodologia, público, território, valor, módulo. Sem abstração.",
    "resumo-expandido": "Máximo 600 palavras. Inclua todas as seções principais em síntese. Linguagem direta.",
}


def humanize(text: str, mode: str = "tecnico-cultural", section_context: str = "") -> str:
    """Reescreve trecho com o modo de linguagem indicado."""
    if not text or len(text.strip()) < 20:
        return text

    mode_instructions = MODE_INSTRUCTIONS.get(mode, MODE_INSTRUCTIONS["tecnico-cultural"])
    prompt_template = load_prompt("humanizar_texto.md")

    prompt = (
        prompt_template
        .replace("{mode}", mode)
        .replace("{mode_instructions}", mode_instructions)
        .replace("{section_context}", section_context or "não especificada")
        .replace("{original_text}", text)
    )

    try:
        result = ai_provider.complete(prompt, max_tokens=3000, temperature=0.4)
        # Remove marcadores de IA da resposta
        result = result.strip()
        for marker in ["**Texto reescrito:**", "**Versão melhorada:**", "**Resultado:**"]:
            result = result.replace(marker, "").strip()
        return result
    except Exception as e:
        return f"[Erro na humanização: {e}]\n\n{text}"
