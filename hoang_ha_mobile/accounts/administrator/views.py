from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
from accounts.models import CustomUser as User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class UserListView(generics.ListAPIView):
    # TODO: Admin should have options to search, filter, ordering. See guideline: https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend.
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.filter(block_by=None)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ["full_name","email","phone","sex","birthday","updated_at","block_at","block_by"]
    search_fields = ["full_name","email","phone","sex","birthday","updated_at","block_at","block_by"]
    filterset_fields = ["full_name","email","phone","sex","birthday","updated_at","block_at","block_by"]

