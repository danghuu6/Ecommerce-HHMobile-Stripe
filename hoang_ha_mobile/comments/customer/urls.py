from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CommentListCreateOwner.as_view(), name="list_comment"),
    path('rating/', views.RatingAPIView.as_view(), name="list_create_rating_product"),
    path('<int:comment_id>/', views.CommentDetail.as_view(), name="comment_detail"),
]