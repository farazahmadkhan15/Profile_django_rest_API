from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from profile_api import permissions
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from profile_api import serializers
from profile_api import models


class HelloApiView(APIView):
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        a = [
            'abc', 'def', 'ghi'
        ]

        return Response({'message': 'Hello!', 'list': a})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello!! {name}'
            return Response({'message': message})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        return Response({'method': 'put'})

    def patch(self, request, pk=None):
        return Response({'method': 'patch'})

    def delete(self, request, pk=None):
        return Response({'method': 'delete'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLS using Routers faraz',
            'Provides more functionality with afafa less code hello',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message."""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""

        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserFeedViewSets(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items."""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated
    )
    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""
        serializer.save(user_profile=self.request.user)
