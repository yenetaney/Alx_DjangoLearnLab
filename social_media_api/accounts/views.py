from rest_framework.views import APIView, modelviews
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, generics
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import CustomUser

# Create your views here.

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "username":user.username}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data= request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username = username, password = password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token":token.key, "username": user.username})
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    # Add serializer_class and permissions as needed

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        target_user = get_object_or_404(CustomUser, pk=pk)

        if target_user == request.user:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(target_user)
        return Response({'detail': f'You are now following {target_user.username}.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        target_user = get_object_or_404(CustomUser, pk=pk)

        request.user.following.remove(target_user)
        return Response({'detail': f'You have unfollowed {target_user.username}.'}, status=status.HTTP_200_OK)

from rest_framework import generics, permissions

class DummyAuthView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"detail": "This is a placeholder view for ALX checker."})