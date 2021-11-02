from core.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from core.serializers import UserSerializer
from .permissions import UserPermission
from .services import send_forgot_password_email
from .exceptions import ForgotPasswordInvalidParams
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission | IsAdminUser]
    pagination_class = PageNumberPagination

    @action(detail=False, methods=['post'], url_path='forgot-password', permission_classes=[AllowAny])
    def forgot_password(self, request):
        if 'email' not in request.POST:
            raise ForgotPasswordInvalidParams
        send_forgot_password_email(request.POST['email'])
        return Response({'worked': True})

    @action(detail=False, methods=['post'], url_path='change-forgotten-password', permission_classes=[AllowAny])
    def change_forgotten_password(self, request):
        email = request.POST.get('email', None)
        forgot_password_hash = request.POST['forgot_password_hash']
        new_password = request.POST['new_password']
        User.change_password(email, forgot_password_hash, new_password)
        return Response({'worked': True})
