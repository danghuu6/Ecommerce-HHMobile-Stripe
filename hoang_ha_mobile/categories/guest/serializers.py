
from rest_framework import serializers

from products.models import Product
from categories.models import Category

from ..models import Category
from variants.models import Variant


class ReadCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
        ]

        read_only_fields = [
            "id",
            "name",
        ]


class ShortProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category"
        ]


class ReadDetailCategorySerializer(serializers.ModelSerializer):
    product = ShortProductSerializer()
    # def get_product(self, obj):
    #     print(obj.category)
    #     return obj.id

    class Meta:
        model = Variant
        fields = [
            "id",
            "product",
            "version",
            "color",
            "price",
            "sale",
            "image"
        ]
