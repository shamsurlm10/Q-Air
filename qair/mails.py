import os
from qair import mail
from flask_mail import Message

def send_mail(to: str, subject: str, body: str):
    msg=Message("Password Reset Request", 
                sender="noreply@qair.com", 
                recipients=[to])
    
    msg.subject = subject
    msg.body = body
    mail.send(msg)