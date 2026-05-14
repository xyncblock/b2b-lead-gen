from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Business schemas
class BusinessBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_market: Optional[Dict[str, Any]] = None
    ideal_customer_profile: Optional[str] = None


class BusinessCreate(BusinessBase):
    pass


class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    target_market: Optional[Dict[str, Any]] = None
    ideal_customer_profile: Optional[str] = None
    questionnaire_answers: Optional[Dict[str, Any]] = None


class BusinessRead(BusinessBase):
    id: int
    user_id: int
    questionnaire_answers: Optional[Dict[str, Any]] = None
    research_artifacts: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Lead schemas
class LeadBase(BaseModel):
    company_name: Optional[str] = None
    company_domain: Optional[str] = None
    contact_name: Optional[str] = None
    contact_title: Optional[str] = None
    email: Optional[str] = None
    email_status: Optional[str] = "unknown"
    country: Optional[str] = None
    industry: Optional[str] = None
    quality_score: Optional[float] = 0.0


class LeadRead(LeadBase):
    id: int
    business_id: int
    review_status: str
    created_at: datetime

    class Config:
        from_attributes = True


# Health schema
class HealthStatus(BaseModel):
    status: str
    version: str = "1.0.0"
    timestamp: datetime


class HealthReady(BaseModel):
    database: bool
    redis: bool
    status: str
