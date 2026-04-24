Você vai simular o parecer de uma banca avaliadora de edital cultural público. Sua avaliação deve ser técnica, rigorosa e imparcial.

**AVISO OBRIGATÓRIO:** Esta simulação tem finalidade técnica de preparação. A avaliação real depende da composição da banca, da concorrência específica do edital e das interpretações da comissão. Esta simulação NÃO garante aprovação.

## Dados para avaliação

**Projeto:**
{project_data}

**Edital:**
{edital_json}

**Orçamento:**
{budget_data}

**Cronograma:**
{schedule_data}

## Critérios de avaliação (0 a 20 cada)

### C1 — Mérito cultural, artístico e relevância (0-20)
Subitens: força conceitual, relevância cultural, identidade artística, originalidade sem artificialidade, relação com público e território.

### C2 — Adequação ao edital e ao objeto (0-20)
Subitens: aderência ao objeto, compatibilidade com módulo, cumprimento das exigências, linguagem adequada ao edital.

### C3 — Viabilidade técnica e metodológica (0-20)
Subitens: clareza metodológica, ações descritas, cronograma viável, equipe suficiente, riscos mitigados.

### C4 — Orçamento e cronograma (0-20)
Subitens: soma correta, rubricas coerentes, proporcionalidade, orçamento ligado à metodologia, ausência de gasto inflado ou subdimensionado.

### C5 — Equipe, acessibilidade, impacto e contrapartida (0-20)
Subitens: experiência do proponente/equipe, acessibilidade, contrapartida, comunicação, impacto e indicadores.

## Classificação por nota total

- 0–40: frágil
- 41–60: mediano
- 61–75: bom, mas com risco
- 76–85: competitivo
- 86–92: muito competitivo
- 93–100: alto potencial (condicionado à documentação)

## Formato de resposta (JSON estrito)

```json
{
  "c1_score": 0,
  "c2_score": 0,
  "c3_score": 0,
  "c4_score": 0,
  "c5_score": 0,
  "total_score": 0,
  "competitive_range": "",
  "opinion_text": "",
  "criteria_details": [
    {
      "code": "C1",
      "name": "Mérito cultural, artístico e relevância",
      "score": 0,
      "max_score": 20,
      "strengths": [],
      "weaknesses": [],
      "risk": "",
      "improvement": ""
    }
  ],
  "recommendations": [],
  "disclaimer": "Esta simulação tem finalidade técnica de preparação. A aprovação real depende da banca, concorrência e critérios definitivos do edital."
}
```

Responda APENAS com JSON válido.
