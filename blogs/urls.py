from django.contrib import admin
from django.urls import path, include
import blogging.template_views as blogging_view
from blogging.urls import user_router
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.registry.extend(user_router.registry)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("login/", blogging_view.login),
    path('', blogging_view.home),
    path("<str:topic_name>/<str:blog_title_slug>", blogging_view.show_blog),
    path("<str:topic_name>", blogging_view.list_all_blogs_wrt_topic),
    path('api/v1/', include(router.urls)),
]
