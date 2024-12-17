from rest_framework import serializers
from .models import Workboards

class WorkboardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workboards
        fields = ('id', 'name', 'creator')
        
