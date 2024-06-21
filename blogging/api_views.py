from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from blogging.models import User
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.custom_response import APIResponse
from django.db import transaction
from django.contrib.auth.hashers import check_password, make_password
from utils.decorators import try_except_rollback_handler
from utils.helper import cipher, decipher
from blogging.models import Blog
from blogging.dal import like_a_blog


class UserViewSet(viewsets.GenericViewSet):

    @action(detail=False, methods=['post'], authentication_classes=[], permission_classes=[])
    def token(self, request: Request) -> APIResponse:
        class RequestSerializer(serializers.Serializer):
            email = serializers.EmailField(required=True)
            password = serializers.CharField(required=True)
        
        request_serializer = RequestSerializer(data=request.data)
        
        if request_serializer.is_valid():
            user = User.objects.filter(email=request_serializer.data.get('email')).first()
            if user and check_password(request.data.get('password'), user.password):
                refresh = RefreshToken.for_user(user)
                return APIResponse(data={'refresh_token': cipher(str(refresh)), 'access_token': cipher(str(refresh.access_token))}, status=status.HTTP_200_OK)
            return APIResponse(success=False, message="Invalid username or password.", status=status.HTTP_401_UNAUTHORIZED)
        else:
            return APIResponse(success=False, message=request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'], authentication_classes=[], permission_classes=[])
    def refresh_token(self, request: Request) -> APIResponse:
        class RequestSerializer(serializers.Serializer):
            refresh_token = serializers.CharField(required=True)
        
        request_serializer = RequestSerializer(data=request.data)
        
        if request_serializer.is_valid():
            try:
                refresh = decipher(RefreshToken(request_serializer.data['refresh_token']))
                return APIResponse(data={'access_token': cipher(str(refresh.access_token))}, status=status.HTTP_200_OK)
            except:
                return APIResponse(success=False, message="Invalid refresh token.", status=status.HTTP_401_UNAUTHORIZED)
        else:
            return APIResponse(success=False, message=request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'], authentication_classes=[], permission_classes=[])
    @try_except_rollback_handler
    def register(self, request):
        class RequestSerializer(serializers.Serializer):
            name = serializers.CharField(min_length=3)
            email = serializers.EmailField(min_length=3)
            password = serializers.CharField(min_length=8)

        request_serializer = RequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return APIResponse(success=False, message=request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User()
        user.name = request_serializer.data['name']
        user.email = request_serializer.data['email']
        user.password = make_password(request_serializer.data['password'])
        user.save()

        refresh = RefreshToken.for_user(user)
        return APIResponse(data={'refresh_token': str(refresh), 'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)


class BlogViewSet(viewsets.GenericViewSet):

    @action(detail=False, methods=['post'])
    @try_except_rollback_handler
    def like_blog(self, request):
        class RequestSerializer(serializers.Serializer):
            title_slug = serializers.SlugField()
    
        request_serializer = RequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return APIResponse(success=False, message=request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

        blog = Blog.objects.get(title_slug=request_serializer.data['title_slug'])
        like_a_blog(blog=blog, user=request.user)
        return APIResponse(data="Done", status=status.HTTP_200_OK)