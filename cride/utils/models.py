# Django models utilities

# Django
from django.db import models

class CRideModel(models.Model):
    """Comparte Ride base model.

    CRideModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created (DateTime): Store the datetime the objects was created
        + modified (DateTime): Store the last datetime the objects was modified
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add = True
        help_text='Date time on which the object was ccreated.'
        )
    modified = models.DateTimeField(
        'modified at',
        auton_now = True
        help_text='Date time on which the object was modified.'
        )

    class Meta:
        """Meta option."""

        abstract = True # Do not create a table in the DB for this class 

        get_lasted_by = 'created'
        orderinng = ['-created', '-modified']