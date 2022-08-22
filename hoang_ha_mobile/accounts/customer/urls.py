from django.urls import path
from . import views
urlpatterns = [
    path('logout/', views.TokenBlacklistView.as_view(), name='logout'),
    path('refresh-token/', views.TokenRefreshView.as_view(), name='refresh_token'),
    path('profile/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('profile/addresses/', views.AddressListCreateAPIView.as_view(), name='create_addrress_list'),
    path('profile/addresses/<int:address_id>/', views.AddressRetrieveDestroyUpdateAPIView.as_view(), name='update_retrieve_destroy_address'),
    path('profile/', views.ProfileUpdateRetrieveAPIView.as_view(), name='detail-profile'),
    path('profile/image/', views.UploadImageAPIView.as_view(), name='upload_image'),
]