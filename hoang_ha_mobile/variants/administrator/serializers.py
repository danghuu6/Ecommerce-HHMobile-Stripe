
from rest_framework import serializers

from variants.models import Variant
from products.models import Product


#serializer for GET Product in Variant
class ProductReadInVariantSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields =[
            'id',
            'name',
            'insurance',
            'category',
            'status',
        ]


#serializer for GET Variant
class VariantReadSerializer(serializers.ModelSerializer):
    product = ProductReadInVariantSerializer(read_only= True)
    class Meta:
        model = Variant
        fields = [
            'id',
            'product',
            'color',
            'version',
            'image',
            'size',
            'strap',
            'general',
            'utilities',
            'network',
            'storage',
            'os_cpu',
            'front_cam',
            'camera',
            'pin',
            'screen',
            'price',
            'sale',
            'status',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            #'deleted_at',
            # 'deleted_by', 
        ]


#Serializer for POST, PUT, DELETE Variant
class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            'id',
            'product',
            'color',
            'version',
            'image',
            'size',
            'strap',
            'general',
            'utilities',
            'network',
            'storage',
            'os_cpu',
            'front_cam',
            'camera',
            'pin',
            'screen',
            'price',
            'sale',
            'status',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
        ]


