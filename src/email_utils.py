from email import encoders
from email.mime.base import MIMEBase
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.settings import *

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    def attachment_file(file_path, file_name):
        with open(file_path, "rb") as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={file_name}')
            msg.attach(part)
    attachment_file(SITE_LOG_PATH,"site_debug.log")
    attachment_file(EXCEL_FILE_PATH,"test_cases.xlsx")

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()
