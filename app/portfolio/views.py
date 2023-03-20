from portfolio.models import Character
from portfolio.serializers import CharacterSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication


class CharacterViewSet(viewsets.ModelViewSet):
    """
    View to CRUD characters
    Only reading is open to public
    """
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

    def get_permissions(self):
        if not self.request.method == 'GET':
            permissions = [IsAuthenticated, IsAdminUser]
            return [permission() for permission in permissions]

        return super().get_permissions()

    def get_authenticators(self):
        if not self.request.method == 'GET':
            authenticators = [TokenAuthentication]
            return [authenticator() for authenticator in authenticators]

        return super().get_authenticators()
