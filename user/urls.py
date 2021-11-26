from django.urls import path, include
from rest_framework.routers import SimpleRouter

from user.views import UserViewSet

app_name = 'user'

router = SimpleRouter()

router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include((router.urls)))
]
