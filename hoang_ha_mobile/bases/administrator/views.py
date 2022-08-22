# Rest framework library
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.response import Response
# Djangoo Filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
# Simple JWT Authenication
from rest_framework_simplejwt.authentication import JWTAuthentication


class BaseModelViewSet(ModelViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        return super().get_queryset().filter(deleted_by=None)

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user,
                        created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        is_paginate = bool(request.query_params.get("paginate",False) == 'true')
        if is_paginate:
            return super().list(request, *args, **kwargs)
        instances = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(instances, many=True)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)