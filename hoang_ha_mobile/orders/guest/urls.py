from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.CreateOrderApiView.as_view()),
    path('<int:order_id>/', views.OrderDetailApiView.as_view())
]