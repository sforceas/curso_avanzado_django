"""Circle membership views"""

# Django REST Framwork
from rest_framework import viewsets,mixins
from rest_framework.generics import get_object_or_404

# Serializers
from cride.circles.serializers.memberships import MembershipModelSerializer

# Models
from cride.circles.models import Circle, Membership

# Permissions
from cride.circles.permissions import IsCircleAdmin,IsActiveCircleMember,IsAdminOrMembershipOwner
from rest_framework.permissions import IsAuthenticated

class MembershipViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Circle membership viewset"""

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the circle exists"""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle,slug_name=slug_name)
        return super(MembershipViewSet,self).dispatch(request, *args, **kwargs)
    
    def get_permissions(self):
        """Assign permissions based on action"""        
        if self.action in ['delete']:
            permissions=[IsAdminOrMembershipOwner]
        else:
            permissions = [IsAuthenticated,IsActiveCircleMember]
        return [p() for p in permissions] 

    def get_queryset(self):
        """Return circle active memberships"""
        return Membership.objects.filter(
            circle=self.circle,
            is_active=True)
    
    def get_object(self):
        """Return the circle member by using the user's username"""
        return get_object_or_404(
            Membership,
            user__username=self.kwargs['pk'],
            circle=self.circle
        )
    
    def perform_destroy(self,instance):
        """Disable membership instead of delete"""
        instance.is_active = False
        instance.save()