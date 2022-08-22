# TODO: @all: Always check the imports list in a consistence format.
from rest_framework import serializers
from variants.models import Variant
from products.models import Product
from .. import models

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "insurance"
        ]

class VariantSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Variant
        fields = [
            "id",
            "product",
            "image",
            "color",
            "version",
            "price",
            "sale"
        ]

class CartReadSerializer(serializers.ModelSerializer):
    variant = VariantSerializer()
    class Meta:
        model = models.Cart
        fields = [
            "id",
            "variant",
            "quantity",
        ]
        # exclude = []
        
class CartWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = [
            "id",
            "variant",
            "quantity",
        ]
    
        
class CartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = [
            "variant",
            "quantity",
        ]
        read_only_fields = ["variant"]
    def validate_quantity(self, quantity):
        if not (quantity > 0):
            raise serializers.ValidationError("Invalid quantity")
        else:
            return quantity