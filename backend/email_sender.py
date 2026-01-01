import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import os
from dotenv import load_dotenv

load_dotenv()

# 환경변수 불러오기
SMTP_SERVER = os.getenv("MAIL_SERVER", "smtp.naver.com")
SMTP_PORT = int(os.getenv("MAIL_PORT", 465))
SMTP_USER = os.getenv("MAIL_USERNAME")
SMTP_PASSWORD = os.getenv("MAIL_PASSWORD")
SMTP_SENDER = os.getenv("MAIL_FROM")

def send_email_manual(to_email: str, subject: str, html_content: str):
    """
    smtplib를 사용하여 SMTP 프로토콜을 직접 제어하는 함수
    """
    try:
        # 1. 메일 봉투(Envelope) 만들기 - MIME 프로토콜 공부 포인트!
        # MIMEMultipart: 텍스트, 이미지, 파일 등을 담을 수 있는 컨테이너
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = formataddr(("Security Team", SMTP_SENDER)) # 보내는 사람 이름 설정
        msg["To"] = to_email

        # 2. 메일 본문(Body) 만들기
        # HTML 형식을 쓴다고 명시 (MIMEText)
        part = MIMEText(html_content, "html", "utf-8")
        msg.attach(part)

        # 3. SMTP 서버 연결 (Handshake 과정) - 보안 공부 포인트!
        print(f"[*] SMTP 서버 연결 시도: {SMTP_SERVER}:{SMTP_PORT}")
        
        # SSL 보안 연결 (포트 465)
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            # EHLO: 서버에게 "나 왔어, 통신 가능해?"라고 인사하는 명령어
            server.ehlo()
            
            # 로그인 (인증)
            server.login(SMTP_USER, SMTP_PASSWORD)
            
            # 전송 (실제 SMTP 명령: MAIL FROM -> RCPT TO -> DATA)
            server.sendmail(SMTP_SENDER, to_email, msg.as_string())
            
        print(f"[+] 메일 전송 성공: {to_email}")
        return True

    except Exception as e:
        print(f"[-] 메일 전송 실패: {e}")
        return False

        # backend/email_sender.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("MAIL_SERVER", "smtp.naver.com")
SMTP_PORT = int(os.getenv("MAIL_PORT", 465))
SMTP_USER = os.getenv("MAIL_USERNAME")
SMTP_PASSWORD = os.getenv("MAIL_PASSWORD")
SMTP_SENDER = os.getenv("MAIL_FROM")

# [수정] tracking_id를 인자로 받아서 이미지 태그를 심음
def send_email_manual(to_email: str, subject: str, html_content: str, tracking_id: str):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = formataddr(("Security Team", SMTP_SENDER))
        msg["To"] = to_email

        # ---------------------------------------------------------
        # [핵심] 트래킹 픽셀(이미지) 심기
        # 실제로는 우리 서버 주소여야 함 (로컬 테스트라 localhost 사용)
        # ---------------------------------------------------------
        tracking_url = f"http://localhost:8000/api/track/open/{tracking_id}"
        tracking_pixel = f'<img src="{tracking_url}" width="1" height="1" style="display:none;" />'
        
        # 원래 본문 뒤에 투명 이미지를 붙임
        final_content = html_content + tracking_pixel
        
        part = MIMEText(final_content, "html", "utf-8")
        msg.attach(part)

        print(f"[*] SMTP Connecting to {SMTP_SERVER}...")
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_SENDER, to_email, msg.as_string())
            
        print(f"[+] Mail Sent to {to_email}")
        return True

    except Exception as e:
        print(f"[-] Mail Failed: {e}")
        return False