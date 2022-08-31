from rest_framework import serializers
from .models import Order


class UpdateChargeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['charge_status']
