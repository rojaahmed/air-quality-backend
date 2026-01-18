import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = "noreply@airhealth.com"
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("GMAIL_ADRESI", "APP_PASSWORD")
    server.send_message(msg)
    server.quit()
