Analise o orçamento do projeto cultural abaixo e identifique problemas, inconsistências e riscos.

## Dados

**Valor total pretendido:** R$ {intended_budget}
**Módulo:** {selected_module}

**Itens do orçamento:**
{budget_items}

**Seções do projeto (resumo):**
{project_summary}

**Regras orçamentárias do edital:**
{orcamento_rules}

## Verificações obrigatórias

1. A soma dos itens bate com o valor total pretendido
2. Existe rubrica de acessibilidade com valor real (não zero)
3. Existe rubrica de comunicação com valor real (não zero)
4. Existe rubrica de equipe/recursos humanos
5. Existe rubrica de registro/documentação
6. Os valores são compatíveis com mercado local
7. Nenhum item é superdimensionado sem justificativa
8. Nenhum item essencial está ausente
9. A equipe no orçamento corresponde à equipe descrita na metodologia
10. Percentuais por categoria estão adequados

## Formato de resposta (JSON estrito)

```json
{
  "total_orcado": 0.0,
  "total_pretendido": 0.0,
  "diferenca": 0.0,
  "status_soma": "ok|excede|abaixo",
  "percentuais": {
    "recursos_humanos": 0.0,
    "servicos": 0.0,
    "materiais": 0.0,
    "comunicacao": 0.0,
    "acessibilidade": 0.0,
    "registro": 0.0,
    "outros": 0.0
  },
  "alertas": [
    {
      "nivel": "critico|medio|leve",
      "item": "",
      "problema": "",
      "sugestao": ""
    }
  ],
  "itens_ausentes": [],
  "itens_questionaveis": [],
  "recomendacao": ""
}
```

Responda APENAS com JSON válido.
