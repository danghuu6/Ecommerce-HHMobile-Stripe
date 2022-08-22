from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ListTagApiView.as_view())
]