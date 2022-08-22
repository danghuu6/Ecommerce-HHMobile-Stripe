
from rest_framework import generics

from .serializers import ReadProductSerializer, ReadDetailProductSerializer
from ..models import Product



class ListProductApiView(generics.ListAPIView):
    serializer_class = ReadProductSerializer
    pagination_class = None

    def get_queryset(self):
        return Product.objects.filter(status=True, deleted_by=None, category=self.request.query_params.get('category')).select_related('category')


class DetailProductApiView(generics.RetrieveAPIView):
    serializer_class = ReadDetailProductSerializer
    queryset = Product.objects.filter(status=True, deleted_by=None)
    lookup_url_kwarg = 'product_id'
