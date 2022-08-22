# Django rest framework imports
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
#Applications imports
from .serializers import VariantSerializer, VariantReadSerializer
from variants.models import Variant
from comments.models import Comment
from comments.administrator.views import CommentViewSet
# Python imports
from datetime import datetime


class VariantViewSet(viewsets.ModelViewSet):
    serializer_class = {
        "list": VariantReadSerializer,
        "retrieve": VariantReadSerializer,
        "create": VariantSerializer,
        "update": VariantSerializer,
        "delete": VariantSerializer
    }
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['product__name']
    filterset_fields = ['product__name', 'status', 'color', 'version', 'front_cam',
                        'camera', 'pin', 'screen', 'storage', 'size', 'price', 'sale', 'network']

    def get_serializer_class(self):
        return self.serializer_class[self.action]

    def get_queryset(self):
        if self.request.method == 'GET':
            return Variant.objects.exclude(deleted_at__isnull=False).select_related('product').order_by('updated_at')
        return Variant.objects.exclude(deleted_at__isnull=False).order_by('updated_at')

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
        comment_view = CommentViewSet()
        comment_view.request = self.request
        comments = Comment.objects.filter(variant=instance)
        for comment in comments:
            comment_view.perform_destroy(comment)
        instance.save()
