# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# [수정됨] 실제 환경변수(env)에서 확인한 아이디/비번/서비스명으로 변경
# mysql+pymysql://아이디:비번@서비스명:포트/DB이름
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DB_URL", 
    "mysql+pymysql://mail_user:mail_password@mysql:3306/mail_security_db"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()