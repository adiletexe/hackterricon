from django.conf import settings
from django.core.mail import send_mail

def send_email(email, token):
    try:
        subject = 'Verify your email'
        message = f'Hi, thank you for registering in ApartX Cleaning. Here is your code to verify your account: ****.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        return False

    return False
