from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("", views.ListCreateSetupIntentViewSet, 'setup-intent-list-create')

urlpatterns = [
    path('', include(router.urls)),
    path('webhooks/', views.webhook, name='webhook')
]