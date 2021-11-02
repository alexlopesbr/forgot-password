from django.conf.urls import url, include
from django.urls import path
from .views import UserViewSet
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', UserViewSet)


urlpatterns = [
    url(r'^auth/?$', views.obtain_auth_token),
    path('', include(router.urls)),
]
