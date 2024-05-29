from django.shortcuts import render
from beaker.cache import cache_region
import blogging.dal as blogging_dal


@cache_region('5_min', 'get_topics')
def get_topics():
    return blogging_dal.get_active_topics_and_total_blogs()
    


def nav_bar_data(request):
    return {
        'topics_list': get_topics()
    }


def home(request):
    context = {
        **nav_bar_data(request=request)
    }
    return render(request, "home.html", context=context)


def list_all_blogs_wrt_topic(request, topic_name):
    all_blogs = blogging_dal.get_active_blogs_wrt_topic(topic_name)
    context = {
        'all_blogs': all_blogs,
        **nav_bar_data(request=request)
    }
    return render(request, "blog_list.html", context=context)