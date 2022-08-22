from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.ListVariantOfProductApiView.as_view()),
    path('<int:variant_id>/', views.RetrieveVariantApiView.as_view())
]