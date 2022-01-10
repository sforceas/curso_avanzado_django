"""Membership model."""

# Django
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL

# Utilities
from cride.utils.models import CRideModel

class Membership(CRideModel):
    """Membership model.
    
    A membership is the table that holds the relationship
    between a user and a circle.
    """
    user = models.ForeignKey('users.User',on_delete=CASCADE)
    profile = models.ForeignKey('users.Profile',on_delete=CASCADE)
    circle = models.ForeignKey('circles.Circle',on_delete=CASCADE)

    is_admin = models.BooleanField(
        'Circle admin',
        default=False,
        help_text="Circle admins can update the circle's data and manage its members")
    
    # Invitations
    used_invitations = models.PositiveSmallIntegerField(default=0)
    remaining_invitations = models.PositiveSmallIntegerField(default=0)   
    invited_by = models.ForeignKey('users.User',null=True,on_delete=SET_NULL,related_name='invited_by')

    # Stats
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)

    # Status
    is_active = models.BooleanField(
        'active status',
        default=True,
        help_text='Only active members are allowed to interact in the circle.'
    )

    def __str__(self):
        """Return username and circle"""
        return '@{} at #{}'.format(self.user.username,self.circle.slug_name)