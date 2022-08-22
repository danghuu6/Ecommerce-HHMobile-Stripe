# Python Datetime
from datetime import datetime
# Model
from products.models import Product
from products.administrator.views import ProductViewSet
from categories.models import Category
# Serializer
from categories.administrator.serializers import CategorySerializer
# BaseModelViewSet 
from bases.administrator.views import BaseModelViewSet

FIELDS = [
    "id",
    "name",
    "status",
    "created_by__email",
    "created_by__phone",
    "created_at",
    "updated_by__email",
    "updated_by__phone",
    "updated_at"
]
class CategoryViewSet(BaseModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().select_related('updated_by','created_by')
    ordering_fields = FIELDS
    search_fields = FIELDS
    filterset_fields = FIELDS
    
    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user
        instance.deleted_at = datetime.now()
        instance.name += "/" + str(instance.deleted_at)
        products = Product.objects.filter(category=instance)
        product_view = ProductViewSet()
        product_view.request = self.request
        for product in products:
            product_view.perform_destroy(instance=product)
        instance.save()