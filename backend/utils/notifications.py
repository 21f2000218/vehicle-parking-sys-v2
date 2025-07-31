from app.extensions import mail
from flask_mail import Message
from flask import current_app

def send_email(to_email, subject, html_content):
    msg = Message(subject, recipients=[to_email], html=html_content)
    mail.send(msg)