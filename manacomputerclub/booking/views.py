from datetime import datetime, timedelta
import json
from pyexpat.errors import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from booking.models import Order
from mana.models import Computers, Services


@login_required
def index(request):
    all_services = Services.objects.all()

    data_ajax = request.GET.get('data', None)

    if request.method == 'POST':
        club = request.POST.get('club')
        service = request.POST.get('service')
        day = request.POST.get('day')
        time = request.POST.get('time')

        # Store day and service in django session:
        selected_service = Services.objects.get(title=service)

        request.session['club'] = club
        request.session['day'] = day
        request.session['time'] = time
        request.session['service'] = service
        request.session['service_duration'] = selected_service.duration
        request.session['service_sum'] = selected_service.sum

        return redirect('booking:submit', permanent=True)

    all_computers = Computers.objects.all().values('id', 'title', 'room')
    data = {
        'computers': list(all_computers)
    }

    context = {
        'data': json.dumps(data),
        'services': all_services,
    }

    return render(request, 'booking/html/booking.html', context)


def booking_submit(request):
    block_list = []
    all_services = Services.objects.all()
    user = request.user
    today = datetime.now()

    # Get stored data from django session:
    day = request.session.get('day')
    time = request.session.get('time')
    service = request.session.get('service')
    club = request.session.get('club')
    duration = request.session.get('service_duration')
    service_sum = request.session.get('service_sum')

    num_computers = request.POST.get('total-computers')
    selected_computers = request.POST.get('selected-computers-input')

    if request.method == 'POST':
        total_sum = int(service_sum) * int(num_computers)

        Order.objects.get_or_create(
            user_id=user.id,
            club=club,
            day=day,
            time=time,
            time_ordered=today,
            num_computers=num_computers,
            services=service,
            total_sum=total_sum,
            count_services=1,
            duration=duration,
        )

        list_selected_computers = selected_computers.split(",")
        for computer_title in list_selected_computers:
            computer = Computers.objects.get(title=computer_title)
            order = Order.objects.latest('id')
            e = Order.objects.get(id=order.id)
            computer.order_set.add(e)

        return redirect('booking:success')

    # Отображение компьютеров
    service_room = Services.objects.get(title=service)

    orders = Order.objects.filter(club=club).exclude(computers=None)
    selected_time = datetime.strptime(time, '%H:%M').time()
    selected_date = datetime.strptime(day, '%Y-%m-%d').date()
    selected_duration_seconds = int(duration) * 60

    selected_datetime = datetime.combine(selected_date, selected_time)
    selected_unix_time = selected_datetime.timestamp()

    for o in orders:
        order = get_object_or_404(Order, id=o.id)
        computers2 = order.computers.all()

        if o.time is not None or o.day is not None:
            order_duration_seconds = int(o.duration) * 60
            order_datetime = datetime.combine(o.day, o.time)
            order_unix_time = order_datetime.timestamp()
            order_total_unix_time = order_unix_time + order_duration_seconds
            computers_titles = [computer.title for computer in computers2]

            if int(order_unix_time) <= int(selected_unix_time) < int(order_total_unix_time) or int(order_total_unix_time) > (int(selected_unix_time) + selected_duration_seconds) > int(order_unix_time):
                block_list += computers_titles

    if service_room.room == "default":
        computers = Computers.objects.filter(room='default').exclude(title__in=block_list).values('id', 'title', 'room')
    elif service_room.room == "vip":
        computers = Computers.objects.filter(room='vip').exclude(title__in=block_list).values('id', 'title', 'room')
    else:
        computers = Computers.objects.filter(room='premium').exclude(title__in=block_list).values('id', 'title', 'room')

    data = {
        'computers': list(computers),
    }

    start_datetime = datetime.strptime(f'{day} {time}', '%Y-%m-%d %H:%M')
    minutes = int(duration)
    duration_timedelta = timedelta(minutes=minutes)
    end_datetime = start_datetime + duration_timedelta

    context = {
        'data': json.dumps(data),
        'services': all_services,
        'day': day,
        'time': time,
        'end_time': end_datetime.strftime('%Y-%m-%d %H:%M'),
        'service': service,
        'club': club,
        'duration': duration,
        'sum': service_sum,
    }  # передача компьютеров в js

    return render(request, 'booking/html/bookingComputers.html', context)


def booking_success(request):
    return render(request, 'booking/html/bookingComplete.html')


def get_available_computers(request):
    # 1 - получаем данные из ajax запроса о клубе, дате, времени, услуге
    selected_club = request.GET.get('club')
    selected_day = request.GET.get('day')
    selected_time = request.GET.get('time')
    selected_service = request.GET.get('service')

    # 2 - Получить список доступных компьютеров, исходя из клуба, даты, времени, услуги
    # if selected_club and selected_day and selected_time and selected_service:

    selected_service_all = Services.objects.get(title=selected_service)

    selected_time_obj = datetime.strptime(selected_time, '%H:%M').time()
    selected_date_obj = datetime.strptime(selected_day, '%Y-%m-%d').date()

    orders = Order.objects.filter(club=selected_club).exclude(computers=None)
    block_list = []
    selected_duration_seconds = int(selected_service_all.duration) * 60

    selected_datetime = datetime.combine(selected_date_obj, selected_time_obj)
    selected_unix_time = selected_datetime.timestamp()

    for o in orders:
        order = get_object_or_404(Order, id=o.id)
        computers2 = order.computers.all()

        if order.time is not None and o.day is not None:
            order_duration_seconds = int(o.duration) * 60
            order_datetime = datetime.combine(o.day, o.time)
            order_unix_time = order_datetime.timestamp()
            order_total_unix_time = order_unix_time + order_duration_seconds

            computers_titles = [computer.title for computer in computers2]

            if int(order_unix_time) <= int(selected_unix_time) < int(order_total_unix_time) or int(order_total_unix_time) > (int(selected_unix_time) + selected_duration_seconds) > int(order_unix_time):
                block_list += computers_titles

    if selected_service_all.room == "default":
        computers = Computers.objects.filter(room='default').exclude(title__in=block_list).values('id', 'title', 'room')
    elif selected_service_all.room == "vip":
        computers = Computers.objects.filter(room='vip').exclude(title__in=block_list).values('id', 'title', 'room')
    else:
        computers = Computers.objects.filter(room='premium').exclude(title__in=block_list).values('id', 'title', 'room')

    # 3 - вернуть обратно список доступных компьютеров
    computers_list = list(computers)
    data = {
        'aviable_computers': list(computers_list),
    }
    return JsonResponse(data)
