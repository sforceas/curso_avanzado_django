"""Circles permission classes"""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Membership

class IsCircleAdmin(BasePermission):
    """Allows access only for circle admins"""
    def has_object_permission(sels,request,view,obj):
        """Verify user has a membership in the object"""
        try: 
            Membership.objects.get(
            user=request.user,
            circle=obj,
            is_admin=True,
            is_active=True
        )
        except Membership.DoesNotExist:
            return False
        return True