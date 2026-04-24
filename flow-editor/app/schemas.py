from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


class ProjectCreate(BaseModel):
    internal_name: str
    public_title: Optional[str] = None
    proponent_name: str
    proponent_cpf_cnpj: Optional[str] = None
    proponent_type: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    cultural_language: Optional[str] = None
    modality: Optional[str] = None
    selected_module: Optional[str] = None
    intended_budget: Optional[float] = None
    duration_months: Optional[int] = None
    observations: Optional[str] = None


class ProjectUpdate(BaseModel):
    internal_name: Optional[str] = None
    public_title: Optional[str] = None
    proponent_name: Optional[str] = None
    proponent_cpf_cnpj: Optional[str] = None
    proponent_type: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    cultural_language: Optional[str] = None
    modality: Optional[str] = None
    selected_module: Optional[str] = None
    intended_budget: Optional[float] = None
    duration_months: Optional[int] = None
    observations: Optional[str] = None
    status: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    internal_name: str
    public_title: Optional[str]
    proponent_name: str
    proponent_type: Optional[str]
    city: Optional[str]
    state: Optional[str]
    cultural_language: Optional[str]
    modality: Optional[str]
    selected_module: Optional[str]
    intended_budget: Optional[float]
    duration_months: Optional[int]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BriefingCreate(BaseModel):
    free_text: Optional[str] = None
    territory: Optional[str] = None
    target_audience: Optional[str] = None
    team_artists: Optional[str] = None
    planned_actions: Optional[str] = None
    desired_spaces: Optional[str] = None
    cultural_references: Optional[str] = None
    confirmed_partners: Optional[str] = None
    desired_partners: Optional[str] = None
    proponent_history: Optional[str] = None
    needed_materials: Optional[str] = None
    desired_accessibility: Optional[str] = None
    desired_counterpart: Optional[str] = None


class SectionUpdate(BaseModel):
    section_name: str
    content: str


class BudgetItem(BaseModel):
    item: str
    category: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    quantity: float = 1.0
    unit_value: float = 0.0
    total_value: float = 0.0
    justification: Optional[str] = None
    related_action: Optional[str] = None


class BudgetResponse(BaseModel):
    id: int
    item: str
    category: Optional[str]
    description: Optional[str]
    unit: Optional[str]
    quantity: float
    unit_value: float
    total_value: float
    justification: Optional[str]
    related_action: Optional[str]

    class Config:
        from_attributes = True


class ScheduleItem(BaseModel):
    phase: str
    month: Optional[str] = None
    activity: Optional[str] = None
    responsible: Optional[str] = None
    evidence: Optional[str] = None


class AuditFinding(BaseModel):
    level: str  # critico, medio, leve, sugestao
    category: str
    location: str
    problem: str
    impact: str
    suggestion: str


class AuditResponse(BaseModel):
    score: float
    status: str
    findings: List[AuditFinding]
    summary: str


class ScoreCriterion(BaseModel):
    code: str
    name: str
    score: float
    max_score: float
    strengths: List[str]
    weaknesses: List[str]
    risk: str
    improvement: str


class ScoreSimulationResponse(BaseModel):
    c1_score: float
    c2_score: float
    c3_score: float
    c4_score: float
    c5_score: float
    total_score: float
    competitive_range: str
    opinion_text: str
    recommendations: List[str]
    criteria_details: List[ScoreCriterion]


class EdictExtracted(BaseModel):
    nome_edital: str = "NÃO IDENTIFICADO AUTOMATICAMENTE — REVISAR MANUALMENTE"
    orgao_responsavel: str = "NÃO IDENTIFICADO AUTOMATICAMENTE — REVISAR MANUALMENTE"
    objeto: str = "NÃO IDENTIFICADO AUTOMATICAMENTE — REVISAR MANUALMENTE"
    periodo_inscricao: str = "NÃO IDENTIFICADO AUTOMATICAMENTE — REVISAR MANUALMENTE"
    quem_pode_participar: List[str] = []
    quem_nao_pode_participar: List[str] = []
    modulos: List[Any] = []
    criterios_avaliacao: List[Any] = []
    bonificacoes: List[str] = []
    documentos_obrigatorios: List[str] = []
    documentos_condicionais: List[str] = []
    anexos: List[str] = []
    regras_orcamento: List[str] = []
    exigencias_acessibilidade: List[str] = []
    exigencias_contrapartida: List[str] = []
    exigencias_comunicacao: List[str] = []
    prazos_execucao: List[str] = []
    prestacao_contas: List[str] = []
    riscos_formais: List[str] = []
    campos_nao_identificados: List[str] = []


class GenerateProjectRequest(BaseModel):
    project_id: int
    regenerate_sections: Optional[List[str]] = None


class HumanizeRequest(BaseModel):
    text: str
    mode: str = "tecnico-cultural"
    section_context: Optional[str] = None


class SettingsUpdate(BaseModel):
    key: str
    value: str
