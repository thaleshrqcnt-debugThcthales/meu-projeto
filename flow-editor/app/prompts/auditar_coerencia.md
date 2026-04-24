Analise o projeto cultural abaixo e identifique todas as inconsistências internas, riscos documentais e pontos de melhoria.

## Dados para auditoria

**Dados do projeto:**
{project_data}

**Seções geradas:**
{sections_text}

**Orçamento:**
{budget_data}

**Cronograma:**
{schedule_data}

**Edital extraído:**
{edital_json}

## O que verificar

### A. Identidade
- Título consistente em todas as seções
- Nome do proponente consistente
- Modalidade e linguagem coerentes

### B. Módulo e valor
- Valor total do orçamento bate com valor pretendido
- Nenhuma seção cita valor divergente
- Módulo citado no texto bate com módulo escolhido

### C. Cronograma
- Datas coerentes e em ordem lógica
- Comunicação antecede execução
- Acessibilidade prevista antes das ações públicas
- Prestação de contas no final

### D. Orçamento
- Soma correta
- Rubricas compatíveis com ações descritas
- Acessibilidade com verba real
- Comunicação com verba real
- Equipe coerente com entrega prometida

### E. Equipe
- Número de pessoas no resumo bate com equipe listada
- Equipe da metodologia aparece no orçamento
- Funções essenciais presentes (produção, comunicação, acessibilidade, registro)

### F. Público
- Público por ação soma com meta geral
- Indicadores de público são mensuráveis

### G. Acessibilidade
- Libras se prometido → orçamento tem Libras
- Audiodescrição se prometida → orçamento tem audiodescrição
- Acessibilidade arquitetônica mencionada

### H. Contrapartida
- Tem ação pública definida
- Tem público, local e duração
- Tem metodologia e comprovação

### I. Território
- Território aparece na justificativa, metodologia e comunicação
- Afirmações fortes têm fonte ou são marcadas como percepção

### J. Marcadores proibidos
- "como modelo de linguagem", "texto gerado", "versão adaptada", "conforme solicitado", "este projeto foi elaborado", "[inserir]", "[preencher]", "XXX", "rascunho", "placeholder"

## Formato de resposta (JSON estrito)

```json
{
  "score": 0,
  "status": "REVISAR ANTES DE ENVIAR",
  "summary": "",
  "findings": [
    {
      "level": "critico|medio|leve|sugestao",
      "category": "identidade|valor|cronograma|orcamento|equipe|publico|acessibilidade|contrapartida|territorio|linguagem",
      "location": "nome da seção afetada",
      "problem": "descrição objetiva do problema",
      "impact": "consequência possível para o projeto",
      "suggestion": "correção específica recomendada"
    }
  ]
}
```

Status possíveis: "APTO PARA EXPORTAR", "APTO COM RESSALVAS", "REVISAR ANTES DE ENVIAR", "ALTO RISCO DOCUMENTAL"

Score: 0 a 100 (coerência documental)

Responda APENAS com JSON válido.
