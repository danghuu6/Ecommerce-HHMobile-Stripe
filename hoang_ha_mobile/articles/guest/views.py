from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ReadArticleSerializer, ListArticleSerializer
from ..models import Article


class ListArticleApiView(generics.ListAPIView):
    serializer_class = ListArticleSerializer
    queryset = Article.objects.filter(status=True, deleted_by=None).select_related(
        "author").prefetch_related("tags")
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["title"]
    # TODO: @Trung: The filter set fields must be usable, it's seem that we only need tags__id or  tags__name.
    filterset_fields = ["tags__name"]


class RetrieveApiView(generics.RetrieveAPIView):
    serializer_class = ReadArticleSerializer
    queryset = Article.objects.filter(
        status=True, deleted_by=None).select_related("author")
    lookup_url_kwarg = "article_id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.viewers += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
