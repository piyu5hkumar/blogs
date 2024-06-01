from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from blogging.models import User
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.custom_response import APIResponse
from django.db import transaction
from django.contrib.auth.hashers import check_password, make_password


class UserViewSet(viewsets.GenericViewSet):

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def token(self, request: Request) -> APIResponse:
        class RequestSerializer(serializers.Serializer):
            email = serializers.EmailField(required=True)
            password = serializers.CharField(required=True)
        
        request_serializer = RequestSerializer(data=request.data)
        
        if request_serializer.is_valid():
            user = User.objects.filter(email=request_serializer.data.get('email')).first()
            if user and check_password(request.data.get('password'), user.password):
                refresh = RefreshToken.for_user(user)
                return APIResponse(data={'refresh_token': str(refresh), 'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
            return APIResponse(success=False, message="Invalid username or password.", status=status.HTTP_401_UNAUTHORIZED)
        else:
            return APIResponse(success=False, message=request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def refresh_token(self, request: Request) -> APIResponse:
        class RequestSerializer(serializers.Serializer):
            refresh_token = serializers.CharField(required=True)
        
        request_serializer = RequestSerializer(data=request.data)
        
        if request_serializer.is_valid():
            try:
                refresh = RefreshToken(request_serializer.data['refresh_token'])
                return APIResponse(data={'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
            except:
                return APIResponse(success=False, message="Invalid refresh token.", status=status.HTTP_401_UNAUTHORIZED)
        else:
            return APIResponse(success=False, message=request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    