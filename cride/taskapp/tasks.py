"""Celery tasks"""

# Django
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

# Celery
from celery.decorators import task

# Models
from cride.users.models import User

# JSON Web Token 
import jwt

#Utilities
from datetime import timedelta

@task(name='send_confirmation_email',max_retries=3)
def send_confirmation_email(user_pk):
    """Send account verification link to the given user"""
    user = User.objects.get(pk=user_pk)
    verification_token=gen_verification_token(user)
    subject='Welcome @{}! Verify your account to start using Comparte Ride'.format(user.username)
    from_email = 'Comparte Ride <noreply@comparteride.com'
    content = render_to_string(
        'emails/users/account_verification.html',
        {'token':verification_token, 'user':user}
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()
    print("Sending email")

def gen_verification_token(user):
    """Generate an account verification JWT token"""
    exp_date = timezone.now()+timedelta(days=3)
    payload = {
        'user':user.username,
        'exp':int(exp_date.timestamp()),
        'type':'email_confirmation'
    }
    token = jwt.encode(payload,settings.SECRET_KEY, algorithm = 'HS256')
    return token