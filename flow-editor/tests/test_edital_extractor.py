"""Testes do extrator de edital — sem chamadas de IA."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from unittest.mock import patch
from app.services.edital_extractor import _normalize_structure, EMPTY_STRUCTURE, NOT_FOUND


SAMPLE_EDITAL_JSON = {
    "nome_edital": "Edital de Fomento à Cultura Municipal 2024",
    "orgao_responsavel": "Secretaria Municipal de Cultura",
    "objeto": "Apoio a projetos de produção artística",
    "periodo_inscricao": "01/03/2024 a 31/03/2024",
    "quem_pode_participar": ["Pessoa física", "MEI", "Associações"],
    "quem_nao_pode_participar": ["Empresas com dívidas públicas"],
    "modulos": [
        {"nome": "Módulo I", "valor": "R$ 30.000", "quantidade_vagas": "20", "descricao": "Pequeno porte"}
    ],
    "criterios_avaliacao": [
        {"codigo": "C1", "nome": "Mérito Cultural", "pontuacao": "30", "descricao": "Relevância cultural"}
    ],
    "documentos_obrigatorios": ["RG/CPF", "Comprovante de residência"],
    "documentos_condicionais": ["Alvará se usar espaço público"],
    "bonificacoes": [],
    "anexos": [],
    "regras_orcamento": ["Vedado uso para equipamentos acima de 30%"],
    "exigencias_acessibilidade": ["Plano de acessibilidade obrigatório"],
    "exigencias_contrapartida": ["1 ação pública gratuita"],
    "exigencias_comunicacao": ["Identidade visual com logo do município"],
    "prazos_execucao": ["6 meses a partir da assinatura"],
    "prestacao_contas": ["Até 30 dias após encerramento"],
    "riscos_formais": ["Documentação incompleta gera inabilitação"],
    "campos_nao_identificados": [],
}


class TestNormalizeStructure:
    def test_all_fields_present(self):
        result = _normalize_structure(SAMPLE_EDITAL_JSON)
        assert result["nome_edital"] == "Edital de Fomento à Cultura Municipal 2024"
        assert len(result["modulos"]) == 1
        assert result["modulos"][0]["nome"] == "Módulo I"

    def test_missing_field_gets_default(self):
        partial = {"nome_edital": "Edital Teste"}
        result = _normalize_structure(partial)
        assert result["orgao_responsavel"] == NOT_FOUND
        assert result["quem_pode_participar"] == []

    def test_list_field_non_list_converted(self):
        data = {"quem_pode_participar": "Todos os artistas"}
        result = _normalize_structure(data)
        assert isinstance(result["quem_pode_participar"], list)

    def test_empty_structure_preserved(self):
        result = _normalize_structure({})
        for key in EMPTY_STRUCTURE:
            assert key in result


class TestEditalExtractorMocked:
    def test_extract_with_mocked_ai(self):
        with patch("app.services.edital_extractor.ai_provider") as mock_ai:
            mock_ai.complete_json.return_value = SAMPLE_EDITAL_JSON
            from app.services.edital_extractor import extract_edict
            result = extract_edict("Texto de edital de teste para extração. " * 50)
            assert result["nome_edital"] == "Edital de Fomento à Cultura Municipal 2024"
            assert len(result["documentos_obrigatorios"]) == 2

    def test_empty_text_returns_structure(self):
        from app.services.edital_extractor import extract_edict
        result = extract_edict("")
        assert isinstance(result, dict)
        assert "nome_edital" in result

    def test_short_text_returns_structure(self):
        from app.services.edital_extractor import extract_edict
        result = extract_edict("Texto curto")
        assert isinstance(result, dict)
        assert "campos_nao_identificados" in result
