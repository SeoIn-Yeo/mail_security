# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# .env에서 DB 정보 가져오기
DB_USER = os.getenv("MYSQL_USER", "user")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
DB_HOST = "mysql"  # 도커 서비스 이름 (localhost 아님!)
DB_PORT = "3306"
DB_NAME = os.getenv("MYSQL_DATABASE", "mail_security_db")

# DB 접속 주소 완성
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 엔진 생성 (커넥션 풀 관리)
engine = create_engine(DATABASE_URL)

# 세션 생성기 (실제 DB 작업용)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델들이 상속받을 기본 클래스 (Base)
Base = declarative_base()