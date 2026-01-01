# backend/models.py
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from database import Base  # 이제 이 코드가 database.py를 찾아갈 수 있습니다! ✅

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    recipient = Column(String(255), nullable=False)
    subject = Column(String(255))
    status = Column(String(50))
    sent_at = Column(DateTime, default=datetime.now)
    error_message = Column(Text, nullable=True)