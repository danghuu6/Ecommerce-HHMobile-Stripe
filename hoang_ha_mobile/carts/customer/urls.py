from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CartOwnerListCreateOrUpdateAPIView.as_view(), name="add_and_list_item"),
    path('<int:cart_id>/', views.CartOwnerUpdateOrDeleteAPIView.as_view(), name="delete_and_update_item"),
    path('listadd/', views.CartListAddAPIView.as_view(), name="add_list_item"),
]