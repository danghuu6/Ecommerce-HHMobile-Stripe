from rest_framework import serializers
from tags.models import Tag
from accounts.administrator.serializers import UserSerializer

class TagSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "status",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at"
        ]
    