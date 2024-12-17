from rest_framework import serializers
from .models import Tasklists

class TasklistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasklists
        fields = ('id', 'name', 'creator')
        
