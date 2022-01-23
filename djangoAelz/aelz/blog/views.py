from django.shortcuts import render
from django.template import Context, Template


def index(request):
    # return HttpResponse('Welcome to BLOG PUPU-HUHa')
    # return render(request, 'blog/home.html', {})
    return render(request, 'blog/index.html', {})



