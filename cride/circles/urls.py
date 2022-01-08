"""Circles URLs"""

# Django
from django.urls import path
from django.urls.conf import include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from cride.circles.views import circles as circles_views

router = DefaultRouter()
router.register(r'circles',circles_views.CircleViewSet,basename='circle')
urlpatterns = [
    path('',include(router.urls))
]


