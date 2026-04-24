from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    internal_name = Column(String(200), nullable=False)
    public_title = Column(String(300), nullable=True)
    proponent_name = Column(String(300), nullable=False)
    proponent_cpf_cnpj = Column(String(30), nullable=True)
    proponent_type = Column(String(50), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(50), nullable=True)
    cultural_language = Column(String(100), nullable=True)
    modality = Column(String(100), nullable=True)
    selected_module = Column(String(200), nullable=True)
    intended_budget = Column(Float, nullable=True)
    duration_months = Column(Integer, nullable=True)
    observations = Column(Text, nullable=True)
    status = Column(String(50), default="rascunho")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    edicts = relationship("Edict", back_populates="project", cascade="all, delete-orphan")
    sections = relationship("ProjectSection", back_populates="project", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="project", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="project", cascade="all, delete-orphan")
    audits = relationship("Audit", back_populates="project", cascade="all, delete-orphan")
    score_simulations = relationship("ScoreSimulation", back_populates="project", cascade="all, delete-orphan")
    exports = relationship("Export", back_populates="project", cascade="all, delete-orphan")
    briefings = relationship("Briefing", back_populates="project", cascade="all, delete-orphan")


class Edict(Base):
    __tablename__ = "edicts"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    filename = Column(String(300), nullable=False)
    raw_text = Column(Text, nullable=True)
    extracted_json = Column(JSON, nullable=True)
    page_count = Column(Integer, nullable=True)
    extraction_status = Column(String(50), default="pendente")
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="edicts")


class Briefing(Base):
    __tablename__ = "briefings"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    free_text = Column(Text, nullable=True)
    territory = Column(Text, nullable=True)
    target_audience = Column(Text, nullable=True)
    team_artists = Column(Text, nullable=True)
    planned_actions = Column(Text, nullable=True)
    desired_spaces = Column(Text, nullable=True)
    cultural_references = Column(Text, nullable=True)
    confirmed_partners = Column(Text, nullable=True)
    desired_partners = Column(Text, nullable=True)
    proponent_history = Column(Text, nullable=True)
    needed_materials = Column(Text, nullable=True)
    desired_accessibility = Column(Text, nullable=True)
    desired_counterpart = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="briefings")


class ProjectSection(Base):
    __tablename__ = "project_sections"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    section_name = Column(String(100), nullable=False)
    content = Column(Text, nullable=True)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="sections")


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    item = Column(String(200), nullable=False)
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    unit = Column(String(50), nullable=True)
    quantity = Column(Float, default=1.0)
    unit_value = Column(Float, default=0.0)
    total_value = Column(Float, default=0.0)
    justification = Column(Text, nullable=True)
    related_action = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="budgets")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    phase = Column(String(200), nullable=False)
    month = Column(String(50), nullable=True)
    activity = Column(Text, nullable=True)
    responsible = Column(String(200), nullable=True)
    evidence = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="schedules")


class Audit(Base):
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    audit_type = Column(String(50), default="coerencia")
    score = Column(Float, nullable=True)
    status = Column(String(50), nullable=True)
    findings_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="audits")


class ScoreSimulation(Base):
    __tablename__ = "score_simulations"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    c1_score = Column(Float, nullable=True)
    c2_score = Column(Float, nullable=True)
    c3_score = Column(Float, nullable=True)
    c4_score = Column(Float, nullable=True)
    c5_score = Column(Float, nullable=True)
    total_score = Column(Float, nullable=True)
    competitive_range = Column(String(50), nullable=True)
    opinion_text = Column(Text, nullable=True)
    recommendations_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="score_simulations")


class Export(Base):
    __tablename__ = "exports"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    file_type = Column(String(20), nullable=False)
    file_path = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="exports")


class AppSettings(Base):
    __tablename__ = "app_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
