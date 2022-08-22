from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from articles.models import Article
from articles.models import Tag
from accounts.administrator.serializers import UserSerializer
from accounts.models import CustomUser as User
from rest_framework.validators import UniqueTogetherValidator


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at"
        ]


class ArticleRetrieveSerializer(serializers.ModelSerializer):
    
    tags = serializers.SerializerMethodField(method_name="get_tags")
    author = UserSerializer()
    updated_by = UserSerializer()

    def get_tags(self, obj):
        tags = obj.tags.filter(deleted_by=None)
        serializer = TagSerializer(instance=tags, many=True)
        return serializer.data

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "description",
            "author",
            "viewers",
            "status",
            "tags",
            "content",
            "image",
            "created_at",
            "updated_by",
            "updated_at"
        ]


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, source="tags", write_only=True
    )

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "description",
            "author",
            "viewers",
            "tag_ids",
            "content",
            "status",
            "image",
            "created_at",
            "updated_by",
            "updated_at",
        ]

        # validators = [
        #     # TODO: @Bang: Article titles can be duplicate, we don't need this validator.
        #     UniqueTogetherValidator(
        #         queryset=Article.objects.filter(deleted_by=None),
        #         fields=["title"]
        #     )
        # ]

    def to_representation(self, instance):
        limit_content = instance.content
        if len(limit_content) > 100:
            limit_content = limit_content[:100]
            instance.content = limit_content
            instance.content += "..."
        return super().to_representation(instance)
