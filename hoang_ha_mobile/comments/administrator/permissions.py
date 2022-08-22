from rest_framework.permissions import IsAdminUser

class IsOwner(IsAdminUser):

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj) and (view.request.user == obj.created_by)

class NotEditedForeignKey(IsAdminUser):
    
    def has_object_permission(self, request, view, obj):
        data = request.data
        check = True
        if ("variant_id" in data) or ("parent_id" in data):
            check = False
        return super().has_object_permission(request, view, obj) and check
