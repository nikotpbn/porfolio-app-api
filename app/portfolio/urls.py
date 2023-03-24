from rest_framework import routers

from portfolio.views import CharacterViewSet, TagViewSet

app_name = 'portfolio'
router = routers.DefaultRouter()

router.register(r'characters', CharacterViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = router.urls
