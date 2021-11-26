from django.urls import path, include
from rest_framework.routers import SimpleRouter

from tire.views import UserTireViewSet

app_name = 'tire'

router = SimpleRouter()

router.register('user-tire-infos', UserTireViewSet, basename='user-tires')

urlpatterns = [
    path('', include((router.urls)))
]
