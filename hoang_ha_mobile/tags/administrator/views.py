# Model
from tags.models import Tag

# Serializer
from tags.administrator.serializers import TagSerializer

# Rest framework library
from rest_framework.response import Response

# Python datetime
from datetime import datetime

# BaseModelViewSet
from bases.administrator.views import BaseModelViewSet

FIELDS = [
    "name",
    "status",
    "created_by__email",
    "created_by__phone",
    "created_at",
    "updated_by__email",
    "updated_by__phone",
    "updated_at"
]


class TagViewSet(BaseModelViewSet):
    queryset = Tag.objects.filter(deleted_by=None).prefetch_related()
    ordering_fields = FIELDS
    search_fields = FIELDS
    filterset_fields = FIELDS
    serializer_class = TagSerializer

    def perform_destroy(self, instance):
        instance.deleted_at = datetime.now()
        instance.name += "/" + str(instance.deleted_at)
        instance.deleted_by = self.request.user
        instance.save()
