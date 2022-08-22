from django.db.models import Q

from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters

from variants.models import Variant

from ..models import Comment
from .serializers import CommentSerializer, RatingSerializer


class ListCommentOfProductApiView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(variant=self.request.query_params.get('variant'), rating=0, parent=None, deleted_by=None)

    def create(self, request, *args, **kwargs):
        request.data['email'] = request.data.get('email').lower()
        return super().create(request, *args, **kwargs)


class ListRatingOfProductApiView(ListCommentOfProductApiView):
    serializer_class = RatingSerializer

    def get_queryset(self):
        return Comment.objects.filter(~Q(rating=0), variant=self.request.query_params.get('variant'), parent=None, deleted_by=None)
