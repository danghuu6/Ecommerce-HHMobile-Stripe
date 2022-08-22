
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ReadVarianSerializer, ReadDetailVarianSerializer
from ..models import Variant


class ListVariantOfProductApiView(generics.ListAPIView):
    serializer_class = ReadVarianSerializer
    queryset = Variant.objects.filter(
        status=True, deleted_by=None).select_related()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["product__name"]
    search_fields = ["product__name", "product__category__name"]


class RetrieveVariantApiView(generics.RetrieveAPIView):
    serializer_class = ReadDetailVarianSerializer
    queryset = Variant.objects.filter(status=True).select_related()
    lookup_url_kwarg = "variant_id"
