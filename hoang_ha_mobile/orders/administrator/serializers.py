
from rest_framework import serializers
from orders.models import Order, OrderDetail
from variants.models import Variant
from variants.administrator.serializers import ProductReadInVariantSerializer


#Serializer for GET Variant in Product
class VariantReadInOrderSerializer(serializers.ModelSerializer):
    product = ProductReadInVariantSerializer(read_only= True)
    class Meta:
        model = Variant
        fields = [
            'id',
            'product',
            'color',
            'version',
            'price',
            'sale',
            'status',
        ]


#serializer GET OrderDetail in Order
class OrderReadDetailSerializer(serializers.ModelSerializer):
    variant = VariantReadInOrderSerializer()
    class Meta:
        model = OrderDetail
        fields =[
            'id',
            'variant',
            'price',
            'quantity',
        ]


#serailizer for GET Order
class OrderReadSerializer(serializers.ModelSerializer):
    number_product = serializers.IntegerField()
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
            'status',
            'total',
            'number_product',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            # 'deleted_at',
            # 'deleted_by',
        ]


#serailizer for GET Retrieve Order
class OrderRetrieveSerializer(serializers.ModelSerializer):
    order_details = OrderReadDetailSerializer(many=True, read_only=True)
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
            'status',
            'total',
            'order_details',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            # 'deleted_at',
            # 'deleted_by',
        ]


#serializer for POST,PUT, DELETE Order 
class OrderSerializer(serializers.ModelSerializer):
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
            'status',
            'total',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',

        ]


#serializer for POST,PUT, DELETE Order Detail 
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields =[
            'id',
            'order',
            'variant',
            'price',
            'quantity',
           
        ]
