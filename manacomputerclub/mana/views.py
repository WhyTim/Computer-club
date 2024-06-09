from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

from booking.models import Order
from mana.models import News, Services

menu = [{'title': "Услуги и компьютеры", 'url_name': 'services'},
        {'title': "Новости", 'url_name': 'news'},
        {'title': "Контакты", 'url_name': 'about'},
        ]


# request содержит информацию о сессияк, куки этого HttpRequest
def index(request):
    news = News.objects.filter(is_published=1)
    data = {
        'news': news,
    }
    return render(request, 'mana/html/index.html', data)


def services(request):
    services = Services.objects.all()
    return render(request, 'mana/html/services.html', {'services': services})


def news(request):
    news = News.objects.filter(is_published=1)
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'news': news,
    }
    return render(request, 'mana/html/news.html', context=data)


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


@login_required
def account(request):
    order = Order.objects.filter(user=request.user).prefetch_related('computers')

    for o in order:
        o.end_datetime, o.formated_end_datetime = calculate_end_datetime(o.day, o.time, o.duration)

    current_datetime = datetime.now()

    context = {
        'data': order,
        'current_datetime': current_datetime,
    }
    return render(request, 'mana/html/account.html', context)


def calculate_end_datetime(day, time, duration):
    start_datetime = datetime.combine(day, time)
    end_datetime = start_datetime + timedelta(minutes=int(duration))
    formatted_end_datetime = end_datetime.strftime('%d.%m.%Y %H:%M')
    return end_datetime, formatted_end_datetime


@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.delete()
        return redirect('account')  # Redirect to the orders page after deletion
    return render(request, 'mana/html/account.html')
