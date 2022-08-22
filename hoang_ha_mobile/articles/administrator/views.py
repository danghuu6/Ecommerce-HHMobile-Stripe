# Model
from articles.models import Article

# Serializer
from articles.administrator.serializers import ArticleSerializer, ArticleRetrieveSerializer

# Permission
from articles.administrator.permissions import IsOwner

# Python datetime
from datetime import datetime

# BaseModelViewSet
from bases.administrator.views import BaseModelViewSet

FIELDS = [
    "id",
    "title",
    "description",
    "viewers",
    "status",
    "content",
    "created_at",
    "author__email",
    "author__phone",
    "updated_by__email",
    "updated_by__phone",
    "updated_at"
]


class ArticleViewSet(BaseModelViewSet):

    ordering_fields = FIELDS
    search_fields = FIELDS
    filterset_fields = FIELDS

    def get_queryset(self):
        if self.action == "retrieve":
            return Article.objects.filter(deleted_by=None).prefetch_related("tags")
        return Article.objects.filter(deleted_by=None).select_related("author", "updated_by")

    def get_permissions(self):
        if self.action != "update":
            return super().get_permissions()
        list_permission = super().get_permissions()
        is_owner = IsOwner()
        list_permission.append(is_owner)
        return list_permission

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ArticleRetrieveSerializer
        return ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user,
                        created_by=self.request.user, author=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted_at = datetime.now()
        # TODO: @Bang: Why we need to update title here? We only need to check the deleted status of it.
        instance.deleted_by = self.request.user
        instance.save()
