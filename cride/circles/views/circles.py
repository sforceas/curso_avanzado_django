"""Circle views"""

# Django REST Framwork
from rest_framework import viewsets

# Serializers
from cride.circles.serializers import CircleModelSerializer

# Models
from cride.circles.models import Circle

class CircleViewSet(viewsets.ModelViewSet):
    queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer
