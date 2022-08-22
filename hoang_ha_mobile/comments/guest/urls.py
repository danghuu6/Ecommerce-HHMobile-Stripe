from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.ListCommentOfProductApiView.as_view()),
    path('rating/', views.ListRatingOfProductApiView.as_view())
]