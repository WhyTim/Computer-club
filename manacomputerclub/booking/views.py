from datetime import datetime, timedelta
import json
from pyexpat.errors import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from booking.models import Order
from mana.models import Computers, Services

# Create your views here.
@login_required
def index(request): 
    all_services = Services.objects.all()

    data_ajax = request.GET.get('data', None)
    print(data_ajax)

    if request.method == 'POST':
        club = request.POST.get('club')
        service = request.POST.get('service')
        day = request.POST.get('day')
        time = request.POST.get('time')
        if service == None:
            messages.success(request, "Please Select A Service!")
            return redirect('order')

        #Store day and service in django session:
        
        selected_service = Services.objects.get(title=service)


        request.session['club'] = club
        request.session['day'] = day
        request.session['time'] = time
        request.session['service'] = service
        request.session['service_duration'] = selected_service.duration
        request.session['service_sum'] = selected_service.sum

        

        # print(club, day, time, service)
        return redirect('booking:submit', permanent=True)
    
    all_computers = Computers.objects.all().values('id', 'title', 'room')
    data = {
        'computers': list(all_computers)
    }
    
    context = {
        'data': json.dumps (data),
        'services': all_services,
    }

    return render(request, 'booking/html/booking.html', context)


def bookingSubmit(request):
    block_list = []
    all_services = Services.objects.all()



    user = request.user
    today = datetime.now()

    #Get stored data from django session:
    day = request.session.get('day')
    time = request.session.get('time')
    service = request.session.get('service')
    club = request.session.get('club')
    duration = request.session.get('service_duration')
    sum = request.session.get('service_sum')
    
    num_computers = request.POST.get('total-computers')
    selected_computers = request.POST.get('selected-computers-input')
    

    if request.method == 'POST':
        total_sum = int(sum) * int(num_computers)
        print(total_sum)
        
        
        

        OrderForm = Order.objects.get_or_create(
                                user_id = user.id,
                                club = club,
                                day = day,
                                time = time,
                                time_ordered = today,
                                num_computers = num_computers,
                                services = service,
                                total_sum = total_sum,
                                count_services = 1,
                                duration = duration,
                                
                            )
        
        
        print(selected_computers.split(","))
        list_selected_computers = selected_computers.split(",")
        for computer_title in list_selected_computers:
            computer = Computers.objects.get(title=computer_title)
            order = Order.objects.latest('id')

            e = Order.objects.get(id=order.id)
            computer.order_set.add(e)
            print(computer_title, "добавлен")

        # selected_computers = request.GET.getlist('selected-computers')
        # print("Выбранные компьютеры", selected_computers)     

        return redirect('booking:success')

    
    # Отображение компьютеров
    
    # computers = Computers.objects.all().values('id', 'title', 'room')
    service_room = Services.objects.get(title=service)
    print(service_room.room)  # выбранная комната default vip
    
    # order = get_object_or_404(Order, id=228)
    # computers2 = order.computers.all()
    
    # result = request.GET.get('result', None)
    # print("Выбранные компьютеры", result)
    # selected_computers = json.loads(result)
    



    orders = Order.objects.filter(club=club).exclude(computers=None)
    selected_time = datetime.strptime(time, '%H:%M').time()
    selected_date = datetime.strptime(day, '%Y-%m-%d').date()
    selected_duration_seconds = int(duration) * 60

    selected_datetime = datetime.combine(selected_date, selected_time)
    selected_unix_time = selected_datetime.timestamp()
    total_unix_time = selected_unix_time + selected_duration_seconds

    print(total_unix_time)
    for o in orders:
        order = get_object_or_404(Order, id=o.id)
        computers2 = order.computers.all()

        print(o.time)
        if o.time != None or o.day != None:
            
            order_duration_seconds = int(o.duration) * 60

            order_datetime = datetime.combine(o.day, o.time)
            order_unix_time = order_datetime.timestamp()
            order_total_unix_time = order_unix_time + order_duration_seconds

            computers_titles = [computer.title for computer in computers2]

            # если попали в промежуток, то говорим, какие компы не отображать
            print(order_datetime, selected_datetime, duration, order_datetime, o.duration)
            print(datetime.fromtimestamp(order_unix_time), datetime.fromtimestamp(selected_unix_time), datetime.fromtimestamp(order_total_unix_time))
            print(int(order_unix_time), int(selected_unix_time), int(order_total_unix_time))
                  
            if int(order_unix_time) < int(selected_unix_time) < int(order_total_unix_time):
                
                block_list+=computers_titles
            
            print([computer.title for computer in computers2], total_unix_time, order_total_unix_time, int(total_unix_time) - int(order_total_unix_time))
            
            # если время заказов order_total_unix_time меньше чем время текущего заказа total_unix_time, то отображаем эти компы
       


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
        'data': json.dumps (data),
        'services': all_services,
        'day': day,
        'time': time,
        'end_time': end_datetime.strftime('%Y-%m-%d %H:%M'),
        'service': service,
        'club': club,
        'duration': duration,
        'sum': sum,
    }  # передача компьютеров в js

    return render(request, 'booking/html/bookingComputers.html', context)


def bookingSuccess(request):

    day = request.session.get('day')
    time = request.session.get('time')
    service = request.session.get('service')
    club = request.session.get('club')
    duration = request.session.get('service_duration')
    sum = request.session.get('service_sum')
    
    return render(request, 'booking/html/bookingComplete.html')


def get_available_computers(request):
    service = request.GET.get('service')
    room = "default" if service == "default" else "vip" if service == "vip" else "premium"

    # Получить все заказы, которые имеют связанные компьютеры
    orders = Order.objects.exclude(computers=None)
    occupied_computers = []

    # for order in orders:
    #     occupied_computers.update(order.computers.all().values_list('id', flat=True))

    # Фильтровать компьютеры в зависимости от типа комнаты и исключить занятые
    computers = Computers.objects.filter(room=room).exclude(id__in=occupied_computers).values('id', 'title', 'room')

    # Преобразование данных в список
    computers_list = list(computers)
    print("Список компьютеров", computers_list)

    return JsonResponse({'computers': computers_list})


def get_data(request):
    """Проверка доступности логина"""
    username = request.GET.get('data', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)