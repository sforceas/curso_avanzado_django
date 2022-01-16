"""Circle membership views"""

# Django REST Framwork
from rest_framework import viewsets,mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
# Serializers
from cride.circles.serializers.memberships import MembershipModelSerializer, AddMembershipSerializer

# Models
from cride.circles.models import Circle, Membership, Invitation


# Permissions
from cride.circles.permissions import IsActiveCircleMember,IsAdminOrMembershipOwner,IsMembershipOwner
from rest_framework.permissions import IsAuthenticated

class MembershipViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.CreateModelMixin,
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
        elif self.action in ['invitations']:
            permissions=[IsMembershipOwner]
        elif self.action in ['create']:
            permissions = [IsAuthenticated]
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
    
    @action(detail=True,methods=['get'])
    def invitations(self,request,*args,**kwargs):
        """Retrieve a member's invitations breakdowns
        
        Will return a list containing all the members that
        have used its invitations and another list containing
        the not used invitations.
        """
        member = self.get_object()
        invited_members = Membership.objects.filter(
            circle=self.circle,
            invited_by=request.user,
            is_active=True,
        )
        unused_invitations = Invitation.objects.filter(
            circle=self.circle,
            issued_by=request.user,
            used=False,
        ).values_list('code')
        print(member)
        print(member.remaining_invitations)
        print()
        # If an admin gives new invitations to the member diff is greater than 0.
        # If diff>0 generate new codes and append it to the lis.
        diff = member.remaining_invitations - len(unused_invitations)
        print(diff)
        invitations = [x[0] for x in unused_invitations]
        for i in range(0,diff):
            print(i)
            invitations.append(
                Invitation.objects.create(
                    issued_by=request.user,
                    circle=self.circle
                ).code
            )

        data = {
            'used_invitations':MembershipModelSerializer(invited_members,many=True).data,
            'invitations':invitations
        }
        return Response(data)

    def create(self,request,*args,**kwargs):
        """Handle membership creation from invitation code"""

        serializer = AddMembershipSerializer(
            data=request.data,
            context={'circle':self.circle,'request':request}
        )
        serializer.is_valid(raise_exception=True)
        member = serializer.save()
        # get_serializer applies the serializer_class from the viewset
        data = self.get_serializer(member).data
        return Response(data,status=status.HTTP_201_CREATED)
