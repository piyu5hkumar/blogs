from django.shortcuts import render
from blogging.template_views import nav_bar_data


def page_not_found(request, exception):
    context = {
        **nav_bar_data(request=request)
    }
    return render(request, "404.html", context=context)