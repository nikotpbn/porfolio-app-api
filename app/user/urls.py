"""
URL mappings for the user API.
"""
from rest_framework import routers

from user.api import views as user_api_views

router = routers.SimpleRouter()

router.register(r'users', user_api_views.UserViewSet)

urlpatterns = router.urls
