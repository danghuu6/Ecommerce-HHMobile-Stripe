from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.ListCategoryApiView.as_view()),
    path('<int:category_id>/', views.DetailCategoryApiView.as_view())
]