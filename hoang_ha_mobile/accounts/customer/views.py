from rest_framework import generics, permissions, response, status
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView
from rest_framework_simplejwt import tokens, authentication
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .. import models
from . import serializers
User = get_user_model()


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return response.Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))            
            self.object.save()
            refresh = tokens.RefreshToken.for_user(self.object)            
            res = {
                'message': 'Password updated successfully',
                'token': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            }
            return response.Response(data=res, status=status.HTTP_200_OK)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AddressListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.AddressSerializer
    pagination_class = None
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        self.queryset = models.Address.objects.filter(user=self.request.user.id)
        return super().get_queryset()
    
    def perform_create(self, serializer):        
        serializer.save(user=self.request.user)
        
        
class AddressRetrieveDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AddressSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    lookup_url_kwarg = 'address_id'
    
    def get_queryset(self):
        self.queryset = models.Address.objects.filter(user=self.request.user.id)
        return super().get_queryset()
    
    
class ProfileUpdateRetrieveAPIView(generics.RetrieveUpdateAPIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if(self.request.method == "GET"):
            self.serializer_class = serializers.ProfileSerializer
        else:
            self.serializer_class = serializers.UserSerializer            
        return super().get_serializer_class()
    
    def get_object(self, queryset=None):
        obj = get_object_or_404(User,id=self.request.user.id)
        return obj    
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.id)
        
        
class UploadImageAPIView(generics.UpdateAPIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserUploadImage

    def get_object(self, queryset=None):
        obj = get_object_or_404(User,id=self.request.user.id)
        return obj    
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.id)