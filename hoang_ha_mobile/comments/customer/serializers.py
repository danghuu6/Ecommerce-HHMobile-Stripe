from rest_framework import serializers

from variants.models import Variant
from .. import models


class ShortInfoProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    
    
class VarianSerializer(serializers.ModelSerializer):
    product = ShortInfoProductSerializer()
    class Meta:
        model = Variant
        fields = [
            "id",
            "product",
            "image",
            "color",
            "version",
        ]

class CommentSerializer(serializers.ModelSerializer):
    variant = VarianSerializer(read_only= True)    
    class Meta:
        model = models.Comment
        fields = [
            "id",
            "name",
            "email",
            "phone",
            # "replies",
            "parent",
            "content",
            "variant",
        ]
    # def get_replies(self, obj):
    #         replies = obj.get_children_comment()
    #         serializer = CommentSerializer(replies, many=True, read_only=True)  
    #         return serializer.data
        
        
class CommentRatingSerializer(serializers.ModelSerializer):
    # replies = CommentReadOnlySerializer(many= True, read_only=True)
    variant = VarianSerializer(read_only= True)
    class Meta:
        model = models.Comment
        fields = [
            "id",
            "name",
            "email",
            "phone",
            # "replies",
            "content",
            "variant",
            "rating",
        ]
        
        
class CommentRatingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = [
            "id",
            "content",
            "rating"
        ]
        