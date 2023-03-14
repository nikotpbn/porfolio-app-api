"""
URL mappings for the user API.
"""
from django.urls import path, include

from rest_framework import routers

from user.api import views as user_api_views

app_name = 'user'

router = routers.DefaultRouter()

router.register(r'users', user_api_views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token', user_api_views.CreateTokenView.as_view(), name='token')
]
