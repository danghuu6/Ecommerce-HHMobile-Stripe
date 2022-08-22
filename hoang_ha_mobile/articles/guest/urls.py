from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.ListArticleApiView.as_view()),
    path('<int:article_id>/', views.RetrieveApiView.as_view())
]