from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Comment

User = get_user_model()


class CreateBySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "image"
        ]


class ReplySerializer(serializers.ModelSerializer):
    created_by = CreateBySerializer()

    class Meta:
        model = Comment
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "content",
            "created_at",
            "created_by",
            "parent"
        ]

        extra_kwargs = {
            'email': {'write_only': True},
            'phone': {'write_only': True},
            'parent': {'write_only': True}
        }


class CommentSerializer(serializers.ModelSerializer):

    replies = serializers.SerializerMethodField()
    # replies = ReplySerializer(many=True, read_only=True)

    created_by = CreateBySerializer(read_only=True)
    # Reply multiple path
    # replies = serializers.SerializerMethodField()
    # def get_replies(self, obj):
    #     queryset = Comment.objects.filter(parent_id=obj.id)
    #     serializer = CommentSerializer(queryset, many=True)
    #     return serializer.data

    def validate_phone(self, value):
        try:
            int(value)
            if (len(value) != 10):
                raise serializers.ValidationError(
                    "phone number is not available")
            return value
        except:
            raise serializers.ValidationError("phone number is not available")

    class Meta:
        model = Comment
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "variant",
            "content",
            "created_at",
            "created_by",
            "replies",
        ]

        extra_kwargs = {
            "email": {"write_only": True},
            "phone": {"write_only": True},
            "variant": {"write_only": True}
        }

    def get_replies(self, instance):
        reply = instance.replies.all().order_by('id')
        return ReplySerializer(reply, many=True).data

class RatingSerializer(serializers.ModelSerializer):

    replies = serializers.SerializerMethodField()
    # replies = ReplySerializer(many=True, read_only=True)

    created_by = CreateBySerializer(read_only=True)
    # Reply multiple path
    # replies = serializers.SerializerMethodField()
    # def get_replies(self, obj):
    #     queryset = Comment.objects.filter(parent_id=obj.id)
    #     serializer = CommentSerializer(queryset, many=True)
    #     return serializer.data

    def validate_phone(self, value):
        try:
            int(value)
            if (len(value) != 10):
                raise serializers.ValidationError(
                    "phone number is not available")
            return value
        except:
            raise serializers.ValidationError("phone number is not available")

    class Meta:
        model = Comment
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "rating",
            "variant",
            "content",
            "created_at",
            "created_by",
            "replies",
        ]

        extra_kwargs = {
            "email": {"write_only": True},
            "phone": {"write_only": True},
            "variant": {"write_only": True}
        }

    def get_replies(self, instance):
        reply = instance.replies.all().order_by('id')
        return ReplySerializer(reply, many=True).data