from portfolio.models import (
    Character,
    Tag,
    Artist,
    Art
)
from portfolio.api.serializers import (
    CharacterSerializer,
    TagSerializer,
    ArtistSerializer,
    ArtSerializer,
    ArtistImageSerializer,
    ArtImageSerializer
)
from core.permissions import IsAuthenticatedAndIsAdminOrReadOnly

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework.authentication import TokenAuthentication

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes
)


class CharacterViewSet(viewsets.ModelViewSet):
    """
    View to CRUD characters
    Only reading is open to public
    """
    permission_classes = [IsAuthenticatedAndIsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

    def get_queryset(self):
        """Retrieve characters filtering  by name when applicable"""
        filter = self.request.query_params.get('name')
        queryset = self.queryset

        if filter:
            queryset = queryset.filter(name__contains=filter)

        return queryset


class TagViewSet(viewsets.ModelViewSet):
    """
    View to CRUD tags
    All endpoints are private
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'name',
                OpenApiTypes.STR,
                description='String or partial string to filter',
            )
        ]
    )
)
class ArtistViewSet(viewsets.ModelViewSet):
    """
    View to CRUD artists
    Only reading is open to public
    """
    permission_classes = [IsAuthenticatedAndIsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def get_queryset(self):
        """Retrieve artists filtering by name when applicable"""
        name = self.request.query_params.get('name')
        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__contains=name)

        return queryset.order_by('id')

    def get_serializer_class(self):
        """return the serializer class for request"""
        if self.action == 'upload_image':
            return ArtistImageSerializer
        if self.action == 'artworks':
            return ArtSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to artist."""
        artist = self.get_object()
        serializer = self.get_serializer(artist, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True)
    def artworks(self, request, pk=None):
        """Fetch Artist related work"""
        artist = self.get_object()
        artworks = artist.artworks.all()
        serializer = self.get_serializer(artworks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of IDs to filter',
            ),
            OpenApiParameter(
                'artist',
                OpenApiTypes.STR,
                description='Comma separated list of IDs to filter'
            )
        ]
    )
)
class ArtViewSet(viewsets.ModelViewSet):
    """
    View to CRUD art
    Only reading is open to public
    """
    permission_classes = [IsAuthenticatedAndIsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]
    queryset = Art.objects.all()
    serializer_class = ArtSerializer

    def _params_to_ints(self, qs):
        """Convert a list of string to integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve arts filtering by tags or artists when applicable"""
        tags = self.request.query_params.get('tags')
        artists = self.request.query_params.get('artists')
        queryset = self.queryset
        if tags:
            tags_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tags_ids)
        if artists:
            artists_ids = self._params_to_ints(artists)
            queryset = queryset.filter(artist__id__in=artists_ids)

        return queryset.order_by('id').distinct()

    def get_serializer_class(self):
        """return the serializer class for request"""
        if self.action == 'upload_image':
            return ArtImageSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to artist."""
        art = self.get_object()
        serializer = self.get_serializer(art, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
