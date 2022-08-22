from rest_framework import serializers
from categories.models import Category
from rest_framework.validators import UniqueTogetherValidator
from accounts.administrator.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "status",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at"
        ]
        # Allow create a category instance again with name value which was removed
        validators = [
            UniqueTogetherValidator(
                queryset = Category.objects.filter(deleted_by = None),
                fields = ["name"]
            )
        ]
