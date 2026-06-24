from rest_framework import serializers
from .models import Income

class IncomeSerializer(serializers.ModelSerializer):
    """Serializes all Income model fields for the REST API."""
    class Meta:
        model = Income
        fields = '__all__'
