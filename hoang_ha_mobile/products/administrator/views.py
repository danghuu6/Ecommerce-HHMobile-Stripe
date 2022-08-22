# Django rest framework imports
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
# Django imports
from django.db.models import Count
# Applications import
from .serializers import ProductSerializer, ProductReadSerializer
from products.models import Product
from variants.models import Variant
from variants.administrator.views import VariantViewSet
# Python imports
from datetime import datetime


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = {
        "list": ProductReadSerializer,
        "retrieve": ProductReadSerializer,
        "create": ProductSerializer,
        "update": ProductSerializer,
        "delete": ProductSerializer
    }

    queryset = Product.objects.exclude(deleted_at__isnull=False).prefetch_related('variants').select_related('category').order_by('updated_at')
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['category__name',
                     'variants__color', 'variants__version', 'name']
    filterset_fields = ['insurance', 'status', 'created_by',
                        'category__name', 'variants__color', 'variants__version']

    def get_serializer_class(self):
        return self.serializer_class[self.action]

    def get_queryset(self):
        if self.request.method == "GET":
            return super().get_queryset().annotate(favorites=Count('favorite'))
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        serializer.save(updated_by=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
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
        instance.deleted_by = self.request.user
        instance.deleted_at = datetime.now()
        instance.name += "/" + str(instance.deleted_at)
        variants = Variant.objects.filter(product=instance)
        variant_view = VariantViewSet()
        variant_view.request = self.request
        for variant in variants:
            variant_view.perform_destroy(variant)
        instance.save()
