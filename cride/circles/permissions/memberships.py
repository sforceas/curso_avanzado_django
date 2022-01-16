"""Membership permissions"""

# Django REST Framework
from lib2to3.pytree import Base
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Membership, memberships

class IsActiveCircleMember(BasePermission):
    """Allow access only to active circle's members
    
    Expect that the views implementing this permissions have
    a 'circle' attribute assigned.
    """
    
    def has_permission(self,request,view):
        """Verify user is an active member of the circle"""
        try:
            Membership.objects.get(
                user=request.user,
                circle=view.circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True

class IsAdminOrMembershipOwner(BasePermission):
    """
    Allow accese only to (Circle's admin) or users
    that are owner of the membership (object).
    """

    def has_permission(self, request, view):
        membership = view.get_object()
        if membership.user == request.user:
            return True

        try:
            Membership.objects.get(
                circle=view.circle,
                user=request.user,
                is_active=True,
                is_admin=True
            )
        except Membership.DoesNotExist:
            return False
        return True

class IsMembershipOwner(BasePermission):
    """Allow access only to membership owner"""
    
    def has_permission(self, request, view):
        """Gets membership as obj and chechs object permission"""
        obj = view.get_object()
        return self.has_object_permission(request,view,obj)
    
    def has_object_permission(self,request,view,obj):
        """Check that the request comes from the membership owner"""
        return request.user==obj.user