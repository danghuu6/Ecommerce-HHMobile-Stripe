from rest_framework import serializers
from . import models

class CommentAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = [
            "name",
            "email",
            "phone",
            "content",
            "product",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
            "deleted_at",
            "deleted_by",
        ]
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = [
            "name",
            "email",
            "phone",
            "content",
            "product",
        ]