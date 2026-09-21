import smtplib
import os
from email.mime.text import MIMEText

GMAIL_ADDRESS = os.environ.get('GMAIL_ADDRESS')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')


def send_otp_email(to_email, otp_code):
    subject = "Your GSMS verification code"
    body = (
        "Hi,\n\n"
        f"Your verification code is: {otp_code}\n\n"
        "This code expires in 10 minutes. If you didn't request this, you can ignore this email.\n\n"
        "- GSMS"
    )
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = GMAIL_ADDRESS
    msg['To'] = to_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, [to_email], msg.as_string())