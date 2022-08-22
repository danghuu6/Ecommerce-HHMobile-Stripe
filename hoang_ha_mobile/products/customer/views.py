from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt import authentication

from django.contrib.auth import get_user_model
User = get_user_model()

from . import serializers
from ..models import Product


class UpdateFavorite(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProductFavorite
    lookup_url_kwarg = 'product_id'
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        self.queryset = Product.objects.all()
        return super().get_queryset()    
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if(self.request.user in instance.favorite.all()):
            data = {
                "favorite": True
            }
        else:
            data = {
                "favorite": False
            }
        serializer = self.get_serializer(instance)
        return Response(data=data, status = status.HTTP_200_OK)
  
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        if(self.request.user in instance.favorite.all()):
            instance.favorite.remove(self.request.user)
        else:
            instance.favorite.add(self.request.user)
            
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

        
class FavoriteListAPIView(generics.ListAPIView):
    serializer_class = serializers.ProductFavoriteListOwner
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    
    def get_queryset(self):
        self.queryset = User.objects.filter(id = self.request.user.id)
        return super().get_queryset()