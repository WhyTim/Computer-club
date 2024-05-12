from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string

# request содержит информацию о сессияк, куки этого HttpRequest
def index(request): 
    # t = render_to_string('mana/html/index.html')
    # return HttpResponse(t)

    return render(request, 'mana/html/index.html')


def news(request, news_id):
    if news_id > 100:
        url_redirect = reverse('news', args=('music', ))
        return redirect(url_redirect)
    return HttpResponse(f"Новости по категориям. id {news_id}")


def news_slug(request, news_slug):
    return HttpResponse(f"Новости по категориям. slug {news_slug}")
