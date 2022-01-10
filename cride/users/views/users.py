"""Users views"""

# Django

#Django REST Framework
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

# Serializers
from cride.users.serializers import UserLoginSerializer, UserModelSerializer, UserSignUpSerializer, AccountVerificationSerializer

class UserViewSet(viewsets.GenericViewSet):
    """User view set.
    Handle sign up, login and account verification.
    """

    @action(detail=False,methods=['post'])
    def signup(self,request):
        """User sign up"""
        serializer=UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data=UserModelSerializer(user).data,
        return Response(data,status=status.HTTP_201_CREATED)

    @action(detail=False,methods=['post'])
    def login(self,request):
        """User log in"""
        serializer=UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data={
            'user': UserModelSerializer(user).data,
            'token':token,
        }
        return Response(data,status=status.HTTP_201_CREATED)

    @action(detail=False,methods=['post'])
    def verify(self,request):
        """Account verification"""
        serializer=AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data={'message':'Congratulations, your account has been verified!'}
        return Response(data,status=status.HTTP_200_OK)