from django.urls import path, include
from .views import OrderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("", OrderViewSet, basename="order")

urlpatterns = [
    path('', include(router.urls)),
]