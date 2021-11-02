from rest_framework.exceptions import APIException
from django.utils.translation import ugettext as _


class ForgotPasswordInvalidParams(APIException):
    status_code = 404
    default_detail = _('Parametros inválidos')
    default_code = 'permission_denied'


class ForgotPasswordExpired(APIException):
    status_code = 404
    default_detail = _('Link expirado')
    default_code = 'permission_denied'


class UserDoesNotExist(APIException):
    status_code = 404
    default_detail = _('Usuário não existe')
    default_code = 'permission_denied'


class InvalidPassword(APIException):
    status_code = 404
    default_detail = _('Senha inválida')
    default_code = 'permission_denied'


class EmailAlreadyTaken(APIException):
    status_code = 404
    default_detail = _('E-mail já cadastrado')
    default_code = 'permission_denied'
