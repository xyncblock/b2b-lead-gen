from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    businesses = relationship("Business", back_populates="owner", cascade="all, delete-orphan")


class Business(Base):
    __tablename__ = "businesses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    target_market = Column(JSON, default=dict)
    ideal_customer_profile = Column(Text)
    questionnaire_answers = Column(JSON, default=dict)
    research_artifacts = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    owner = relationship("User", back_populates="businesses")
    research_jobs = relationship("ResearchJob", back_populates="business", cascade="all, delete-orphan")
    scrape_jobs = relationship("ScrapeJob", back_populates="business", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="business", cascade="all, delete-orphan")
    exports = relationship("CSVExport", back_populates="business", cascade="all, delete-orphan")


class ResearchJob(Base):
    __tablename__ = "research_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    llm_model = Column(String(100))
    total_cost_usd = Column(Float, default=0.0)
    output = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    business = relationship("Business", back_populates="research_jobs")


class ScrapeJob(Base):
    __tablename__ = "scrape_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    status = Column(String(50), default="pending")
    target_count = Column(Integer, default=100)
    found_count = Column(Integer, default=0)
    dedup_count = Column(Integer, default=0)
    config = Column(JSON, default=dict)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    error = Column(Text)
    
    business = relationship("Business", back_populates="scrape_jobs")


class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    scrape_job_id = Column(Integer, ForeignKey("scrape_jobs.id"), nullable=True)
    
    company_name = Column(String(255))
    company_domain = Column(String(255))
    contact_name = Column(String(255))
    contact_title = Column(String(255))
    email = Column(String(255))
    email_status = Column(String(50), default="unknown")  # valid, risky, unknown
    phone = Column(String(50))
    country = Column(String(100))
    region = Column(String(100))
    city = Column(String(100))
    industry = Column(String(100))
    employee_estimate = Column(String(50))
    
    source_url = Column(Text)
    source_type = Column(String(50))  # directory, company_site, serp
    raw_payload = Column(JSON, default=dict)
    dedup_hash = Column(String(64))
    
    review_status = Column(String(50), default="pending")  # pending, approved, rejected
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True))
    quality_score = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    business = relationship("Business", back_populates="leads")
    __table_args__ = (
        UniqueConstraint('business_id', 'dedup_hash', name='uix_lead_dedup'),
    )


class CSVExport(Base):
    __tablename__ = "csv_exports"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    lead_count = Column(Integer, default=0)
    filter_snapshot = Column(JSON, default=dict)
    file_path = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    business = relationship("Business", back_populates="exports")
