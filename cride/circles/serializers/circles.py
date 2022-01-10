"""Circle serializers"""

# Django REST Framework
from typing import ValuesView
from typing_extensions import Required
from rest_framework import serializers

# Model
from cride.circles.models import Circle

class CircleModelSerializer(serializers.ModelSerializer):
    """Circle model serializer"""

    members_limit = serializers.IntegerField(
        required=False,
        min_value=10,
        max_value=3000
    )
    is_limited = serializers.BooleanField(default=False)

    class Meta:
        """Meta class"""
        model = Circle
        fields = (
            'name','slug_name','about','picture',
            'rides_taken','rides_offered',
            'verified','is_public',
            'is_limited','members_limit',
        )
        read_only_fields = (
            'rides_taken',
            'rides_offered',
            'is_public',
            'verified'
        )

    def validate(self,data):
        """Ensure both is_limit and members_limit are present.
        If one of the fields is TRUE and the other is FALSE rise
        Validation Error. Exclusive OR: ^
        """
        members_limit = data.get('members_limit',None)
        is_limited = data.get('is_limited',False)
        if is_limited ^ bool(members_limit):
            raise serializers.ValidationError('If circle is limited, a member limit must be provided.')
        return data
