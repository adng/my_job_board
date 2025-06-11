from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    """
    Serializer for Job model.
    """

    owner = serializers.PrimaryKeyRelatedField(read_only=True)  # Set by view

    class Meta:
        model = Job
        fields = "__all__"
