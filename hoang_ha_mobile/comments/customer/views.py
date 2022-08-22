from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt import authentication

from hoang_ha_mobile.base.errors import check_rating_exist, check_valid_comment

from django.db.models import Q

from django.contrib.auth import get_user_model
User = get_user_model()

from . import serializers
from .. import models


class CommentListCreateOwner(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['variant']
    filterset_fields = ['variant']
    
    def get_queryset(self):               
        self.queryset = models.Comment.objects.filter(created_by = self.request.user.id, rating=0)
        return super().get_queryset()
    
    def create(self, request, *args, **kwargs):
        # comment_instance = models.Comment.objects.filter(variant = self.request.data.get('variant'), id=self.request.data.get('parent'))
        # if(comment_instance.exists()):
        #     return super().create(request, *args, **kwargs)
        # else:
        #     return response.Response(data={"detail": "Comment failed,Error: Different variant or comment parent, Can't create new instance"}, status=status.)
        temp = check_valid_comment(self.request.data.get('parent'), self.request.data.get('variant'))
        if(temp is not None):
            return temp
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)
        
    
class RatingAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CommentRatingSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['variant']
    filterset_fields = ['variant']
    
    def get_queryset(self):    
        self.queryset = models.Comment.objects.filter( ~Q(rating=0),created_by = self.request.user.id)
        return super().get_queryset()
    
    def create(self, request, *args, **kwargs):        
        # rate = models.Comment.objects.filter(~Q(rating=0), created_by=self.request.user.id, variant=self.request.data.get('variant'))
        # if(rate.exists()):    
        #     # TODO: @Toan: All error should be managed in a base/errors.py for all errors of platforms to easier maintain later. Should not use magic errors in all codes.
        #     return response.Response(data={"detail": "Rating existed, Can't create new instance"}, status=status.HTTP_404_NOT_FOUND)
        temp = check_rating_exist(self.request.user.id, self.request.data.get('variant'))
        if(temp is not None):
            return temp
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):            
        serializer.save(created_by=self.request.user, updated_by=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'comment_id'
            
    def get_serializer_class(self):
        if(self.request.method == "GET"):
            self.serializer_class = serializers.CommentRatingSerializer
        if(self.request.method == "PATCH" or self.request.method == "PUT"):
            self.serializer_class = serializers.CommentRatingUpdateSerializer                  
        return super().get_serializer_class()
    
    def get_queryset(self):
        if(self.request.method == "PUT" or self.request.method == "PATCH"):
            self.queryset = models.Comment.objects.filter( ~Q(rating=0), created_by = self.request.user.id)
        else:
            self.queryset = models.Comment.objects.filter(created_by = self.request.user.id)
        return super().get_queryset()
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    

        

