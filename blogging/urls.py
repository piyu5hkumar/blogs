from rest_framework.routers import SimpleRouter
from blogging.api_views import UserViewSet

user_router = SimpleRouter()
user_router.register(r'users', UserViewSet, basename='users')


