
from rest_framework import serializers

from variants.models import Variant
from ..models import Order, OrderDetail


class ShortVariantSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = Variant
        fields = [
            "id",
            "product",
            "color",
            "version",
            "image",
            "price"
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = [
            'order',
            'variant',
            'price',
            'quantity',
        ]

        extra_kwargs = {
            "order": {"write_only": True}
        }


class OrderDetailReadSerializer(serializers.ModelSerializer):
    variant = ShortVariantSerializer()

    class Meta:
        model = OrderDetail
        fields = [
            'variant',
            'price',
            'quantity',
        ]


class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailReadSerializer(many=True, read_only=True)

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
        model = Order
        fields = [
            'id',
            'name',
            'phone',
            'email',
            'shipping',
            'delivery_address',
            'note',
            'total',
            'status',
            'order_details',
        ]


class CancelOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'status'
        ]


class ListOrderSerializer(serializers.ModelSerializer):
    # detail = serializers.SerializerMethodField()

    # def get_detail(self, obj):
    #     queryset = OrderDetail.objects.filter(order = obj.id)
    #     serializer = OrderDetailReadSerializer(queryset, many=True)
    #     print(serializer.data[0])
    #     return serializer.data[0]
    order_details = OrderDetailReadSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'shipping',
            'total',
            'status',
            'order_details'
        ]
