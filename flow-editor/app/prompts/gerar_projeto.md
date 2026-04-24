Com base nos dados do edital, do proponente e do briefing abaixo, gere um projeto cultural completo para inscrição em edital público.

## Dados do projeto

**Edital extraído:**
{edital_json}

**Dados do proponente:**
- Nome: {proponent_name}
- Tipo: {proponent_type}
- Cidade/Estado: {city}/{state}
- Linguagem artística: {cultural_language}
- Modalidade: {modality}
- Módulo pretendido: {selected_module}
- Valor pretendido: R$ {intended_budget}
- Duração: {duration_months} meses

**Briefing livre do projeto:**
{briefing_free_text}

**Informações adicionais fornecidas:**
- Território: {territory}
- Público-alvo: {target_audience}
- Equipe/artistas: {team_artists}
- Ações previstas: {planned_actions}
- Espaços desejados: {desired_spaces}
- Referências culturais: {cultural_references}
- Parceiros confirmados: {confirmed_partners}
- Parceiros desejados (NÃO CONFIRMADOS): {desired_partners}
- Histórico do proponente: {proponent_history}
- Materiais necessários: {needed_materials}
- Acessibilidade desejada: {desired_accessibility}
- Contrapartida desejada: {desired_counterpart}

## Regras de geração

1. **Parceiros desejados ≠ parceiros confirmados.** Se parceiros desejados foram informados, escreva "parceria em articulação" ou "em processo de negociação", nunca como fato consumado.
2. **Espaços desejados ≠ espaços confirmados.** Use "espaço a ser confirmado" ou "local a ser negociado junto à instituição X".
3. **Histórico não comprovado** deve ser apresentado como "trajetória relatada pelo proponente" se não há comprovação.
4. **Não invente** currículos, premiações, aprovações anteriores, dados populacionais ou índices sem fonte.
5. **Cada seção deve ser completa**, com texto pronto para inscrição, sem lacunas marcadas como [inserir].
6. **Linguagem:** técnica, cultural, densa, direta. Sem frases publicitárias. Sem tom escolar se o projeto não for formação.

## Seções a gerar

Gere cada seção no formato:

### [NOME_DA_SECAO]
[Conteúdo completo]

Seções obrigatórias:
1. TITULO
2. RESUMO (máximo 500 palavras)
3. APRESENTACAO
4. JUSTIFICATIVA
5. DIAGNOSTICO_TERRITORIAL
6. OBJETIVO_GERAL
7. OBJETIVOS_ESPECIFICOS
8. PUBLICO_ALVO
9. METAS
10. METODOLOGIA
11. ACOES_PREVISTAS
12. CRONOGRAMA (formato tabular em Markdown)
13. EQUIPE
14. PLANO_ACESSIBILIDADE
15. PLANO_COMUNICACAO
16. CONTRAPARTIDA
17. INDICADORES
18. ORCAMENTO_NARRATIVO
19. RISCOS_MITIGACAO
20. RESULTADOS_ESPERADOS
21. LEGADO
22. CHECKLIST_ANEXOS
23. ADEQUACAO_EDITAL
