from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
import os
from typing import List

# 1. 환경변수에서 메일 설정 가져오기
conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", ""),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", ""),
    MAIL_FROM = os.getenv("MAIL_FROM", ""),
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

# 2. API 요청 바디 모델
class EmailSchema(BaseModel):
    email: List[EmailStr]
    subject: str
    body: str

# 3. 실제 메일 전송 함수 (이게 없어서 에러가 난 겁니다!)
async def send_email_async(email_data: EmailSchema):
    message = MessageSchema(
        subject=email_data.subject,
        recipients=email_data.email,
        body=email_data.body,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"status": "success"}