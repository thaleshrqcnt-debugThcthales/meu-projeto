Com base no edital abaixo, gere um checklist completo de documentos e tarefas para inscrição.

## Edital:
{edital_json}

## Dados do proponente:
- Tipo: {proponent_type}
- Módulo: {selected_module}

## Regras

1. Separe documentos obrigatórios de condicionais (exigidos apenas em alguns casos).
2. Identifique claramente quem deve apresentar cada documento.
3. Especifique o formato quando indicado no edital.
4. Aponte o risco formal de cada documento faltante.
5. Não invente documentos não previstos no edital.

## Formato de resposta (JSON estrito)

```json
{
  "checklist": [
    {
      "documento": "",
      "tipo": "obrigatorio|condicional",
      "condicao": "",
      "quem_apresenta": "",
      "formato": "",
      "prazo": "",
      "status": "nao_iniciado",
      "observacao": "",
      "risco_se_faltar": "desclassificacao|perda_de_nota|advertencia|nao_aplicavel"
    }
  ],
  "tarefas_preparacao": [
    {
      "tarefa": "",
      "prioridade": "alta|media|baixa",
      "prazo_sugerido": ""
    }
  ],
  "alertas": []
}
```

Responda APENAS com JSON válido.
