from ast import Delete
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from tags.models import Tag
from .serializers import TagSerializer

class ListTagApiView(generics.ListAPIView):
    queryset = Tag.objects.filter(deleted_by = None)
    serializer_class = TagSerializer
    pagination_class = None