from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions

# Create your views here.
class HelloApiView(APIView):
    """Test a new APIView"""
    serializer_class = serializers.HelloSerializer
    def get(self, request, format=None):
        """Return a list of APIViews features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'It is similar to a traditional django view',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message':'Hello!','an_apiview':an_apiview})
    def post(self, request):
        """Create a post message with our name"""
        serializer = serializers.HelloSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle updating the object"""
        return Response({'method':'put'})

    def patch(self, request, pk=None):
        """Partially update an object"""
        return Response({'method':'patch'})
    def delete(self, request, pk=None):
        """Deletes an object"""
        return Response({'method':'delete'})

class HelloViewSet (viewsets.ViewSet):
    """test API ViewSet"""
    serializer_class = serializers.HelloSerializer
    def list(self, request):
        """Return a hello message"""
        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code'
        ]
        return Response({'message':'Hello!','a_viewset':a_viewset})
    def create(self,request):
        """Create a new hello message"""
        serializer = serializers.HelloSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self,request, pk=None):
        """"Retreive an object by ID"""
        return Response({'http_method':'GET'})
    def update(self, request, pk=None):
        """Update and update of an object"""
        return Response({'http_method':'PUT'})
    def partial_update(self, request, pk=None):
        """Partial update"""
        return Response({'http_method':'PATCH'})
    def destroy(self, request, pk=None):
        """Destroy an object"""
        return Response({'http_method':'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating, updating and deleteing profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfiles,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)

class LoginViewSet(viewsets.ViewSet):
    """Check email and password and returns an auth token"""
    serializer_class=AuthTokenSerializer
    def create (self, request):
        """Use the ObtainAuthToken APIView to validate and create a token"""
        return ObtainAuthToken().post(request)

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """creating, reading and updating profiles feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)
    def perform_create(self, serializer):
        """ser the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)

@login_required
def home(request):
    return render(request, 'core/home.html')
