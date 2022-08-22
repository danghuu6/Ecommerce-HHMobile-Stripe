# TODO: @all: The code Layout in here look good :). Just handle about imports list. We should follow this styles for all team members. :)
# Django rest framework imports
from rest_framework import viewsets, filters, generics
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
# Django imports
from django.db.models import Sum,Count
# Application imports
from .serializers import OrderSerializer,OrderReadSerializer ,OrderRetrieveSerializer
from orders.models import Order
# Python import
from datetime import datetime


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = {
        "list": OrderReadSerializer,
        "retrieve": OrderRetrieveSerializer,
        "update": OrderSerializer,
        "delete": OrderSerializer
    }
    queryset = Order.objects.exclude(deleted_at__isnull=False).prefetch_related('order_details').order_by('created_at')
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['email','status']
    search_fields = ['email','shipping','status','delivery_address']

    def get_serializer_class(self):
        return self.serializer_class[self.action]
    
    def get_queryset(self):
        if self.request.method == "GET":
            return super().get_queryset().annotate(number_product=Sum('order_details__quantity'))
        return super().get_queryset()

    def perform_create(self, serializer):
       pass
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        data = {
            "id": instance.id,
            "deleted_by": self.request.user.id,
            "deleted_at": datetime.now()
        }
        serializer = OrderSerializer(instance=instance, data=data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
