# backend/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

# 방금 만든 database.py 파일에서 Base를 가져옴
from database import Base

# 1. 관리자
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password_hash = Column(String(255))
    email = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# 2. 수신자 (타겟)
class Target(Base):
    __tablename__ = "targets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    organization = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# 3. 메일 템플릿
class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content_html = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# 4. 캠페인
class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    logs = relationship("CampaignLog", back_populates="campaign")

# 5. 로그 (가장 중요)
class CampaignLog(Base):
    __tablename__ = "campaign_logs"
    id = Column(Integer, primary_key=True, index=True)
    tracking_uuid = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    status = Column(String(20), default="sent") 
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    opened_at = Column(DateTime(timezone=True), nullable=True)
    clicked_at = Column(DateTime(timezone=True), nullable=True)
    
    campaign = relationship("Campaign", back_populates="logs")