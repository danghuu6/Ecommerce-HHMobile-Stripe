from rest_framework.permissions import IsAdminUser

class IsOwner(IsAdminUser):

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj) and (view.request.user == obj.author)
