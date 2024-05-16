from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

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
    return render(request, 'mana/html/news.html')
    # if news > 100:
    #     url_redirect = reverse('news', args=('music', ))
    #     return redirect(url_redirect)


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


def newsid(request, news_id):
    return HttpResponse(f"Новость number: {news_id}")
