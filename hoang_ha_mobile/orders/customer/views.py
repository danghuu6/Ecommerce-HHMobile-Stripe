from rest_framework import generics, permissions, response, status, viewsets
from rest_framework_simplejwt import authentication
from rest_framework.decorators import action
from variants.models import Variant
from hoang_ha_mobile.base.errors import check_valid_item

from . import serializers
from .. import models
from hoang_ha_mobile.base import stripe_base


class ListCreateOrderAPIView(generics.ListCreateAPIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.OrderReadSerializer
    
    def get_queryset(self):        
        self.queryset = models.Order.objects.filter(created_by=self.request.user.id)
        return super().get_queryset()    
    
    def post(self, request, *args, **kwargs):
        serializer = serializers.OrderSerializer(data=request.data.get('order'))   
        array_order_detail = self.request.data.get("order_details")
        temp = check_valid_item(array_order_detail)
        if(temp is not None):
            return temp
        if(serializer.is_valid()):            
            self.instance = serializer.save(created_by=self.request.user)
            instance_price = 0

            temp = check_valid_item(array_order_detail)
            if(temp is not None):
                return temp
            for order_detail in array_order_detail:       
                variant = Variant.objects.get(id=order_detail.get('variant'))
                if(variant.sale > 0):
                    price = variant.sale
                else:
                    price = variant.price
                instance_price += int(price) * int(order_detail.get('quantity'))
                data = {
                    "order": self.instance.id,
                    "variant": order_detail.get('variant'),
                    "quantity": order_detail.get('quantity'),
                    "price": price
                }
                serializer = serializers.OrderDetailSerializer(data=data)
                if(serializer.is_valid()):
                    serializer.save()

            try:
                cus = stripe_base.search_and_create_customer(self.request.user.email)

                intent = stripe_base.payment_intent_create(instance_price, "vnd", self.instance.id, customer=cus['id'])

                self.instance.total = instance_price
                self.instance.save()
                serializer = serializers.OrderSerializer(self.instance)

                return response.Response({'client_secret': intent['client_secret'],
                                        'order_id': intent.metadata['order_id']},
                                        status=status.HTTP_201_CREATED)
            except Exception as e:
                return response.Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
