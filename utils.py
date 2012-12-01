from django.core.mail import EmailMessage
from django.core.mail import send_mail



def send_email():
    email = EmailMessage('Subject', 'Body', to=['laimiux@gmail.com'])
    email.send()
