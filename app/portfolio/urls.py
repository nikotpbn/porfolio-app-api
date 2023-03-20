from rest_framework import routers

from portfolio.views import CharacterViewSet

app_name = 'portfolio'
router = routers.DefaultRouter()

router.register(r'characters', CharacterViewSet)

urlpatterns = router.urls
