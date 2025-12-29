# backend/main.py (수정본)
from fastapi import FastAPI, BackgroundTasks, Request, Depends
# [수정됨] Response와 RedirectResponse는 여기서 가져와야 합니다
from fastapi.responses import Response, RedirectResponse 
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import models
from database import engine, get_db

# email_sender.py에서 함수 가져오기
from email_sender import send_email_async, EmailSchema 

# DB 테이블 생성
models.Base.metadata.create_all(bind=engine)

# 1x1 투명 픽셀 데이터
PIXEL_DATA = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'

app = FastAPI(title="Mail Security API", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Mail Security API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# [Step 2] 메일 전송 기능
@app.post("/api/mail/send")
async def send_mail_endpoint(email_data: EmailSchema):
    await send_email_async(email_data)
    return {"message": "메일 전송 요청 완료!"}

# [Step 3] 추적 기능
@app.get("/api/track/open/{tracking_uuid}")
async def track_open(tracking_uuid: str, db: Session = Depends(get_db)):
    log = db.query(models.CampaignLog).filter(models.CampaignLog.tracking_uuid == tracking_uuid).first()
    if log and not log.opened_at:
        log.opened_at = datetime.now()
        log.status = "opened"
        db.commit()
        print(f"👀 [Open Detected] UUID: {tracking_uuid}")
    return Response(content=PIXEL_DATA, media_type="image/gif")

@app.get("/api/track/click/{tracking_uuid}")
async def track_click(tracking_uuid: str, db: Session = Depends(get_db)):
    log = db.query(models.CampaignLog).filter(models.CampaignLog.tracking_uuid == tracking_uuid).first()
    if log and not log.clicked_at:
        log.clicked_at = datetime.now()
        log.status = "clicked"
        db.commit()
        print(f"👆 [Click Detected] UUID: {tracking_uuid}")
    
    return RedirectResponse(url="https://www.naver.com")