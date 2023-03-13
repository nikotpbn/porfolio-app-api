"""
URL mappings for the user API.
"""
from rest_framework import routers
from user.api.views import UserViewSet

app_name = 'user'

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)

urlpatterns = router.urls
