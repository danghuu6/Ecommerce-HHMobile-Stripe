from datetime import datetime

from comments.models import Comment
from comments.administrator.serializers import CommentSerializer

from comments.administrator.permissions import IsOwner, NotEditedForeignKey

from bases.administrator.views import BaseModelViewSet

FIELDS = [
    "content",
    "phone",
    "name",
    "email",
    "rating",
    "updated_at",
    "created_at"
]
class CommentViewSet(BaseModelViewSet):
    queryset = Comment.objects.filter(deleted_by=None).select_related()
    serializer_class = CommentSerializer
    ordering_fields = FIELDS
    search_fields = FIELDS
    filterset_fields = FIELDS

    def get_permissions(self):
        if self.action != 'update':
            return super().get_permissions()
        list_of_permission = super().get_permissions()
        is_owner = IsOwner()
        not_edited = NotEditedForeignKey()
        list_of_permission.append(is_owner)
        list_of_permission.append(not_edited)
        return list_of_permission 

    def perform_create(self, serializer):
        serializer.save(
            updated_by = self.request.user, 
            created_by = self.request.user,
            name = self.request.user.full_name,
            email = self.request.user.email,
            phone = self.request.user.phone
        )

    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user 
        instance.deleted_at = datetime.now()
        instance.save()