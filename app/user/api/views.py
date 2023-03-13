"""
Views for the user API.
"""

from rest_framework import viewsets

from django.contrib.auth import get_user_model

from user.api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
