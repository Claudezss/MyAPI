from time import sleep
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from flask_app.app import create_celery
import os

celery_app = create_celery()

GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_PASS = os.environ.get("GMAIL_PASS")


@celery_app.task(name="mailer")
def send_email(email_message):
    login = GMAIL_USER
    password = GMAIL_PASS

    sender_email = "zy2269770664@gmail.com"
    receiver_email = "zy2269770664@gmail.com"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Job Finished"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = f"""
    <html>
    <body>
        <p>Hi,<br> your celery job has finished</p>
        <a>Result: {email_message}</a>
    </body>
    </html>
    """
    body = MIMEText(html, "html")
    message.attach(body)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(login, password)
    server.sendmail(sender_email, receiver_email, message.as_string())


@celery_app.task(bind=True)
def test(self):

    for i in range(60):
        self.update_state(state="PROGRESS", meta={"current": i})
        sleep(2)

    return "finished"
