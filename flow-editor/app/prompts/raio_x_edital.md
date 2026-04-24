Analise o texto do edital cultural público fornecido abaixo e extraia todas as informações relevantes no formato JSON especificado.

## Regras de extração

1. **Não complete por imaginação.** Se uma informação não estiver explícita no texto, use: "NÃO IDENTIFICADO AUTOMATICAMENTE — REVISAR MANUALMENTE"
2. **Preserve trechos literais** quando relevante, especialmente critérios de avaliação, requisitos e valores.
3. **Identifique ambiguidades** e liste no campo `campos_nao_identificados`.
4. **Extraia todos os módulos** com seus respectivos valores e vagas.
5. **Mapeie todos os documentos** separando obrigatórios de condicionais.

## Formato de resposta (JSON estrito)

```json
{
  "nome_edital": "",
  "orgao_responsavel": "",
  "objeto": "",
  "periodo_inscricao": "",
  "quem_pode_participar": [],
  "quem_nao_pode_participar": [],
  "modulos": [
    {
      "nome": "",
      "valor": "",
      "quantidade_vagas": "",
      "descricao": ""
    }
  ],
  "criterios_avaliacao": [
    {
      "codigo": "",
      "nome": "",
      "pontuacao": "",
      "descricao": ""
    }
  ],
  "bonificacoes": [],
  "documentos_obrigatorios": [],
  "documentos_condicionais": [],
  "anexos": [],
  "regras_orcamento": [],
  "exigencias_acessibilidade": [],
  "exigencias_contrapartida": [],
  "exigencias_comunicacao": [],
  "prazos_execucao": [],
  "prestacao_contas": [],
  "riscos_formais": [],
  "campos_nao_identificados": []
}
```

Responda APENAS com o JSON válido, sem texto adicional antes ou depois.

## Texto do edital:

{edital_text}
