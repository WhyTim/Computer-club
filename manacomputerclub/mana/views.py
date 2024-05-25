from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

from mana.models import News

menu = [{'title': "Услуги и компьютеры", 'url_name': 'services'},
        {'title': "Новости", 'url_name': 'news'},
        {'title': "Контакты", 'url_name': 'about'},
        ]


# request содержит информацию о сессияк, куки этого HttpRequest
def index(request): 
    # t = render_to_string('mana/html/index.html')
    # return HttpResponse(t)
    return render(request, 'mana/html/index.html')


def services(request):
    return render(request, 'mana/html/services.html')


def news(request):
    news = News.objects.filter(is_published=1)

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'news': news,
        'cat_selected': 0,
    }
    return render(request, 'mana/html/news.html', context=data)

    # if news > 100:
    #     url_redirect = reverse('news', args=('music', ))
    #     return redirect(url_redirect)

def newsid(request, news_id):
    news = get_object_or_404(News, pk=news_id)

    data = {
        'title': news.title,
        'menu': menu,
        'news': news,
        'content': news.content,
        'cat_selected': 1,
    }

    return render(request, 'mana/html/news_content.html', data)

def about(request):
    return render(request, 'mana/html/about.html')

# def login(request):
#     return render(request, 'mana/html/signin.html')


@login_required
def booking(request):
    return render(request, 'mana/html/booking.html')


@login_required
def account(request):
    return render(request, 'mana/html/account.html')



