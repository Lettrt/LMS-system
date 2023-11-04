from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(email, first_name):
    subject = 'Добро пожаловать в наш проект!'
    message = f'Привет, {first_name}! Спасибо за регистрацию в нашем проекте.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

@shared_task
def send_reset_email(email, subject, message):
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])