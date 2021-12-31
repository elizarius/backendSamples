from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, Template


def citizen_kane(request):
    content = """{{movie}} was released in {{year}}"""
    template = Template(content)
    context = Context({"movie": "Citizen Kane", "year": 1941})

    result = template.render(context)
    return HttpResponse(result)

def index(request):
    #return HttpResponse('Welcome to BLOG PUPU-HUHa')
    return render(request, 'blog/home.html', {})


