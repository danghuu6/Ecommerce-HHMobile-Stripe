
from rest_framework import serializers

from variants.models import Variant

from ..models import Product


class VariantReadInProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            'id',
            'image',
            'color',
            'version',
            'price',
            'sale',
            'status',
            'deleted_by'
        ]


class ListImageProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            "id",
            'image',
            'status',
            'deleted_by'
        ]


class ReadProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
        ]

        read_only_fields = [
            "id",
            "name",
            "description",
            "insurance",
            "category"
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


class ReadDetailProductSerializer(serializers.ModelSerializer):
    # product = ShortProductSerializer()

    # def get_product(self, obj):
    #     print(obj.category)
    #     return obj.id
    variants = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        queryset = Variant.objects.filter(product=obj.id)
        serializer = ListImageProductSerializer(queryset, many=True)
        image = []
        for data in serializer.data:
            if(data['status'] == True) and (data['deleted_by'] == None):
                image.append(data['image'])
        return image

    def get_variants(self, obj):
        queryset = Variant.objects.filter(product=obj.id)
        serializer = VariantReadInProductSerializer(queryset, many=True)
        variants = []
        for data in serializer.data:
            if(data['status'] == True) and (data['deleted_by'] == None):
                data.pop('status')
                data.pop('deleted_by')
                variants.append(data)
        return variants

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "image",
            "insurance",
            "variants",
            "description",
        ]
