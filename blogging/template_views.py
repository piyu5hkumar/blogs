from django.shortcuts import render
from django.http import HttpResponseNotFound
from beaker.cache import cache_region
import blogging.dal as blogging_dal
import blogging.models as blogging_models


@cache_region('5_min', 'get_topics')
def get_topics():
    return blogging_dal.get_active_topics_and_total_blogs()
    


def nav_bar_data(request):
    return {
        'topics_list': get_topics()
    }



def page_404(request):
    context = {
        **nav_bar_data(request=request)
    }
    return render(request, "404.html", context=context)



def home(request):
    hot_blogs = blogging_dal.get_hot_blogs(total=3)
    new_blogs = blogging_dal.get_new_blogs(total=3)
    context = {
        'hot_blogs': hot_blogs,
        'new_blogs': new_blogs,
        **nav_bar_data(request=request)
    }
    return render(request, "home.html", context=context)


def list_all_blogs_wrt_topic(request, topic_name):
    all_blogs = blogging_dal.get_active_blogs_wrt_topic(topic_name)
    
    if not all_blogs:
        return page_404(request)


    context = {
        'all_blogs': all_blogs,
        **nav_bar_data(request=request)
    }
    return render(request, "blog_list.html", context=context)


def show_blog(request, topic_name, blog_title_slug):
    blog = blogging_models.Blog.objects.filter(title_slug=blog_title_slug).first()
    context = {
        'title_slug': blog.title_slug,
        'title': blog.title,
        'total_likes': blog.total_likes,
        'total_comments': blog.total_comments,
        'total_shares': 3,
        'content': blog.content,
        **nav_bar_data(request=request)
    }
    return render(request, "blog.html", context=context)


def login(request):
    context = {
        **nav_bar_data(request=request)
    }
    return render(request, "login.html", context=context)