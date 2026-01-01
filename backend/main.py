# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from email_sender import send_email_manual

# database.py와 models.py에서 필요한 것들 가져오기
from database import SessionLocal, engine, Base
import models 

# 1. DB 테이블 자동 생성
models.Base.metadata.create_all(bind=engine)

# 2. 앱 생성 (딱 한 번만 선언해야 함!)
app = FastAPI()

# 3. CORS 설정 (React 연동을 위해 필수)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. DB 세션 의존성 주입
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 5. 데이터 모델 정의
class EmailRequest(BaseModel):
    email: List[str]
    subject: str
    body: str

# 6. API 엔드포인트 정의

@app.post("/api/mail/send")
async def send_mail_endpoint(request: EmailRequest, db: Session = Depends(get_db)):
    results = []
    
    for recipient in request.email:
        print(f"[*] Sending to {recipient}...")
        
        # 메일 전송
        is_success = send_email_manual(recipient, request.subject, request.body)
        
        # DB 저장
        status = "success" if is_success else "fail"
        new_log = models.EmailLog(
            recipient=recipient,
            subject=request.subject,
            status=status,
            error_message=None if is_success else "SMTP Error"
        )
        db.add(new_log)
        db.commit()
        
        results.append({"email": recipient, "status": status})

    return {"message": "Campaign finished", "results": results}

@app.get("/api/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total = db.query(models.EmailLog).count()
    success = db.query(models.EmailLog).filter(models.EmailLog.status == "success").count()
    fail = db.query(models.EmailLog).filter(models.EmailLog.status == "fail").count()
    
    return {
        "total_sent": total,
        "success": success,
        "failed": fail,
        "opened": 0,
        "clicked": 0
    }

    # backend/main.py (전체 덮어쓰기 추천)
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from email_sender import send_email_manual
from datetime import datetime
import uuid # 고유 ID 생성용

from database import SessionLocal, engine, Base
import models 

# DB 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class EmailRequest(BaseModel):
    email: List[str]
    subject: str
    body: str

# 1. 메일 발송 API
@app.post("/api/mail/send")
async def send_mail_endpoint(request: EmailRequest, db: Session = Depends(get_db)):
    results = []
    
    for recipient in request.email:
        # 고유 ID 생성 (주민등록번호 같은 것)
        tracking_id = str(uuid.uuid4())
        
        # 메일 전송 (tracking_id도 같이 넘김)
        is_success = send_email_manual(recipient, request.subject, request.body, tracking_id)
        
        status = "success" if is_success else "fail"
        new_log = models.EmailLog(
            recipient=recipient,
            subject=request.subject,
            status=status,
            tracking_id=tracking_id, # DB에 ID 저장
            error_message=None if is_success else "SMTP Error"
        )
        db.add(new_log)
        db.commit()
        results.append({"email": recipient, "status": status})

    return {"message": "Campaign finished", "results": results}

# 2. [핵심] 트래킹 픽셀 감지 API
# 메일 본문의 이미지가 이 주소를 부르면 실행됨
@app.get("/api/track/open/{tracking_id}")
def track_email_open(tracking_id: str, db: Session = Depends(get_db)):
    print(f"[*] Tracking pixel hit! ID: {tracking_id}")
    
    # DB에서 해당 ID를 가진 로그 찾기
    log = db.query(models.EmailLog).filter(models.EmailLog.tracking_id == tracking_id).first()
    
    if log and not log.opened_at: # 아직 안 읽은 상태라면
        log.status = "opened"     # 상태 변경
        log.opened_at = datetime.now() # 시간 기록
        db.commit()
        print(f"[+] Email opened by {log.recipient}")

    # 투명한 1x1 이미지 데이터 반환 (상대방에겐 깨진 이미지가 안 보이게)
    # 1x1 투명 GIF 바이너리 데이터
    pixel_data = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    return Response(content=pixel_data, media_type="image/gif")

# 3. 대시보드 통계 API
@app.get("/api/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total = db.query(models.EmailLog).count()
    success = db.query(models.EmailLog).filter(models.EmailLog.status == "success").count()
    fail = db.query(models.EmailLog).filter(models.EmailLog.status == "fail").count()
    opened = db.query(models.EmailLog).filter(models.EmailLog.status == "opened").count() # 읽은 개수 추가
    
    return {
        "total_sent": total,
        "success": success,
        "failed": fail,
        "opened": opened,
        "clicked": 0
    }