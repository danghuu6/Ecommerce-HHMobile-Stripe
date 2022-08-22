from rest_framework import serializers

from categories.models import Category
from products.models import Product
from variants.models import Variant

#serializer for GET Category in Product
class CategoryReadInProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "status",
        ]


#Serializer for GET Variant in Product
class VariantReadInProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            'id',
            'color',
            'version',
            'price',
            'sale',
            'status',
        ]


#Serializer for GET LIST Product
class ProductReadSerializer(serializers.ModelSerializer):
    category = CategoryReadInProductSerializer(read_only =True )
    variants = serializers.SerializerMethodField()
    favorites = serializers.IntegerField()
    class Meta:
        model = Product
        fields =[
            'id',
            'name',
            'category',
            'description',
            'insurance',
            'variants',
            'status',
            'favorites',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            #'deleted_at',
            #'deleted_by',
        ]
    
    def get_variants(self, obj):
        variants = Variant.objects.exclude(deleted_at__isnull=False)
        return VariantReadInProductSerializer(variants, many=True, read_only =True).data
 
  
#Serializer for POST, PUT, DELETE Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields =[
            'id',
            'name',
            'description',
            'insurance',
            'category',
            'status',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
        ]


