from django.urls import path, include
from . import views
urlpatterns = [
    path('login/', views.LoginApiView.as_view()),
    path('register/', views.RegisterApiView.as_view()),
    path('forgot-password/', views.ForgotPasswordApiView.as_view()),
    path('reset-password/', views.ChangePasswordWithPINApiView.as_view())
]