from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.ListCreateOrderAPIView.as_view(), name='create_order'),  
     
]