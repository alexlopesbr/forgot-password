from core.models import User
from emails.services import send_email_forgot_password
from .exceptions import UserDoesNotExist
from django.utils import timezone
from datetime import timedelta
import re
import urllib.parse
import urllib.request


def send_forgot_password_email(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise UserDoesNotExist
    now = timezone.now()
    user.forgot_password_hash = re.sub(r'\D', '', str(now))
    user.forgot_password_expire = now + timedelta(hours=24)
    user.save()
    link = 'https://forgot-password.com/change-password?email=%s&hash=%s' % (
        urllib.parse.quote(user.email), user.forgot_password_hash)
    send_email_forgot_password(user.email, link)
