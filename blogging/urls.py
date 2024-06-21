from rest_framework.routers import SimpleRouter
from blogging.api_views import (
    UserViewSet,
    BlogViewSet,
)

user_router = SimpleRouter()
user_router.register(r'users', UserViewSet, basename='users')


blog_router = SimpleRouter()
blog_router.register(r'blogs', BlogViewSet, basename='blogs')


