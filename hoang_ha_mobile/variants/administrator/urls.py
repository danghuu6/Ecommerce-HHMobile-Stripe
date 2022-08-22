from django.urls import path, include
from .views import VariantViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", VariantViewSet, basename="variants")

urlpatterns = [
    path('', include(router.urls))
]