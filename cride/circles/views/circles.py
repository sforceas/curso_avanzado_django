"""Circle views"""

# Django REST Framwork
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Serializers
from cride.circles.serializers import CircleModelSerializer

# Models
from cride.circles.models import Circle

class CircleViewSet(viewsets.ModelViewSet):
    queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer
    permission_classes =(IsAuthenticated,)

    def get_queryset(self):
        """Restrict list to public-only circles
        only if a list is provided.
        If only a single circle is provided 
        do not apply filer.

        """
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset
    