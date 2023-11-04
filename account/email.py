from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tasks import send_reset_email

def send_password_reset_email(user):
    context = {
        'email': user.email,
        'domain': 'https://employeer.ru/',
        'site_name': 'IT Academy EDU',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': default_token_generator.make_token(user),
        'protocol': 'http',
    }
    subject = 'Сброс пароля на сайте'
    email_template_name = 'registration/password_reset_email.html'
    message = render_to_string(email_template_name, context)
    send_reset_email.delay(user.email, subject, message)
