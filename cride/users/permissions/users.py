"""User permissions"""

# Django REST Framwework
from rest_framework.permissions import BasePermission

class IsAccountOwner(BasePermission):
    """Allow access only to objects owned by the requesting user."""
    message = 'You dont have permission to access to this resource'

    def has_object_permission(self,request,view,obj):
        """Check obj and user are the same"""
        return request.user == obj
    