"""Circle views"""

# Django REST Framwork
from rest_framework import viewsets,mixins

# Serializers
from cride.circles.serializers import CircleModelSerializer

# Models
from cride.circles.models import Circle, Membership

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.circles import IsCircleAdmin

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter 
from django_filters.rest_framework import DjangoFilterBackend

class CircleViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
                   
    serializer_class = CircleModelSerializer
    lookup_field = 'slug_name'

   # Filters
    filter_backends = (SearchFilter,OrderingFilter,DjangoFilterBackend)
    search_fields = ('slug_name','name')
    ordering_fields = ('rides_offered','rides_taken','member_limit','created','name')
    ordering = ('-members__count','-rides_offered','-rides_taken')
    filter_fields = ('verified','is_limited')

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
    
    def get_permissions(self):
        """Assign permissions based on an action"""
        permissions = [IsAuthenticated]
        if self.action in ['update','partial_update']:
            permissions.append(IsCircleAdmin)
        return [permission() for permission in permissions]

    def perform_create(self,serializer):
        """Assign circle admin"""
        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10,
        )