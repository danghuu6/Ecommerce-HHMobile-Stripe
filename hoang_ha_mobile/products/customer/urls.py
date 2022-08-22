from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:product_id>/like/', views.UpdateFavorite.as_view()),
    path('list/', views.FavoriteListAPIView.as_view()),
]