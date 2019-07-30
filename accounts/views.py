from django.contrib.auth import get_user_model

from rest_framework import status, mixins, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer

User = get_user_model()

class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a POST request to create a new user.
    """
    def has_permission(self, request, view):
        return bool(
                request.method == 'POST' or
                request.user and 
                request.user.is_authenticated
        )

class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #search_fields = ('full_name', User.USERNAME_FIELD)
    
    permission_classes = [IsAuthenticatedOrCreateOnly]
    #filter_backends = ()

    def list(self, request, *args, **kwargs):
        queryset = User.objects.exclude(auth_token=request.auth)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwards):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        json = serializer.data
        json['token'] = token.key
        headers = self.get_success_headers(serializer.data)
        return Response(json, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        queryset = User.objects.get(auth_token=request.auth)
        serializer = self.get_serializer(queryset, show_access_only=True)
        return Response(serializer.data)

