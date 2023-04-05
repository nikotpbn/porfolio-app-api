from portfolio.models import (
    Character,
    Tag,
    Artist,
    Art
)
from portfolio.serializers import (
    CharacterSerializer,
    TagSerializer,
    ArtistSerializer,
    ArtSerializer
)
from core.permissions import IsAuthenticatedAndIsAdminOrReadOnly

from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework.authentication import TokenAuthentication


class CharacterViewSet(viewsets.ModelViewSet):
    """
    View to CRUD characters
    Only reading is open to public
    """
    permission_classes = [IsAuthenticatedAndIsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    View to CRUD tags
    All endpoints are private
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]


class ArtistViewSet(viewsets.ModelViewSet):
    """
    View to CRUD artists
    Only reading is open to public
    """
    permission_classes = [IsAuthenticatedAndIsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class ArtViewSet(viewsets.ModelViewSet):
    """
    View to CRUD art
    Only reading is open to public
    """
    permission_classes = [IsAuthenticatedAndIsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]
    queryset = Art.objects.all()
    serializer_class = ArtSerializer
