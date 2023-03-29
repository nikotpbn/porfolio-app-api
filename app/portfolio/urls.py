from rest_framework import routers

from portfolio.views import (
    CharacterViewSet,
    TagViewSet,
    ArtistViewSet,
    ArtViewSet
)

app_name = 'portfolio'
router = routers.DefaultRouter()

router.register(r'characters', CharacterViewSet)
router.register(r'tags', TagViewSet)
router.register(r'artists', ArtistViewSet)
router.register(r'arts', ArtViewSet)

urlpatterns = router.urls
