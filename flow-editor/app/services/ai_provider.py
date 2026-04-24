"""
Camada de abstração para provedor de IA.
Suporta Anthropic. Preparado para extensão a OpenAI e Ollama.
"""
import json
import re
from pathlib import Path
from typing import Optional
from app.config import settings


PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def load_prompt(name: str) -> str:
    path = PROMPTS_DIR / name
    if path.exists():
        return path.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Prompt não encontrado: {name}")


def load_system_prompt() -> str:
    return load_prompt("system_base.md")


class AIProvider:
    def __init__(self):
        self.provider = settings.ai_provider
        self.model = settings.ai_model
        self.api_key = settings.anthropic_api_key

    def _get_anthropic_client(self):
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY não configurada. "
                "Configure em .env ou na tela de Configurações."
            )
        import anthropic
        return anthropic.Anthropic(api_key=self.api_key)

    def complete(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 8000,
        temperature: float = 0.3,
    ) -> str:
        if system is None:
            system = load_system_prompt()

        if self.provider == "anthropic":
            return self._anthropic_complete(prompt, system, max_tokens, temperature)
        raise ValueError(f"Provedor de IA não suportado: {self.provider}")

    def _anthropic_complete(self, prompt: str, system: str, max_tokens: int, temperature: float) -> str:
        client = self._get_anthropic_client()
        response = client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def complete_json(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 8000,
    ) -> dict:
        """Solicita resposta JSON e faz parsing."""
        raw = self.complete(prompt, system=system, max_tokens=max_tokens, temperature=0.1)
        return self._parse_json_response(raw)

    def _parse_json_response(self, raw: str) -> dict:
        raw = raw.strip()
        # Remove markdown code fences
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        raw = raw.strip()
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            # Tenta extrair JSON de bloco no meio do texto
            match = re.search(r"\{[\s\S]*\}", raw)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass
            raise ValueError(f"Resposta não é JSON válido: {e}\n\nRaw: {raw[:500]}")


ai_provider = AIProvider()
