from django.core.mail import EmailMessage
from django.conf import settings


def open_and_return(my_file):
    with open(settings.BASE_DIR + '/emails/templates/' + my_file, 'r', encoding="utf-8") as file:
        data = file.read()
    return data


def send_email_forgot_password(email, link):
    template = open_and_return("forgot-password.html").format(link)

    msg = EmailMessage(
        u'Email forgot password received',
        template,
        to=[email, ],
        from_email=settings.EMAIL_HOST_USER
    )

    msg.content_subtype = 'html'
    msg.send()
