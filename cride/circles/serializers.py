"""Circle serializers."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from cride.circles.models.circles import Circle

class CircleSerializer(serializers.Serializer):
    """Circle serializer."""

    name = serializers.CharField()
    slug_name = serializers.SlugField()
    rides_taken = serializers.IntegerField()
    rides_offered = serializers.IntegerField()
    members_limit=serializers.IntegerField()

class CreateCircleSerializer(serializers.Serializer):
    """Creae circle serializer"""

    name = serializers.CharField(max_length=140)
    slug_name = serializers.SlugField(
        max_length=40,
        validators=[
            UniqueValidator(queryset=Circle.objects.all())
        ]
    )
    about = serializers.CharField(
        max_length=255,
        required=False
    )

    """Override create() method to make it save the model into the DB"""
    def create(self,data):
        """Create circle in DB"""
        return Circle.objects.create(**data)