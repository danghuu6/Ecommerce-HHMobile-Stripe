# TODO: @all: check the Code Lay-out here. All spacing between classes, functions must be consistent. See guidelines: https://peps.python.org/pep-0008/. We need to refactor on all codes.
from rest_framework import generics
from variants.models import Variant

from .serializers import ReadCategorySerializer, ReadDetailCategorySerializer
from ..models import Category


class ListCategoryApiView(generics.ListAPIView):
    serializer_class = ReadCategorySerializer
    queryset = Category.objects.filter(status=True, deleted_by=None)
    pagination_class = None


class DetailCategoryApiView(generics.ListAPIView):
    serializer_class = ReadDetailCategorySerializer

    def get_queryset(self):
        return Variant.objects.filter(
            deleted_by=None, status=True, product__category=self.kwargs.get('category_id'))
