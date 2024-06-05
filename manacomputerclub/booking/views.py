from datetime import datetime
import json
from pyexpat.errors import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from booking.models import Order
from mana.models import Computers, Services

# Create your views here.
@login_required
def index(request): 
    all_services = Services.objects.all()

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
    
    return render(request, 'booking/html/booking.html', {'services': all_services})


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
    print(service_room.room)
    
    # order = get_object_or_404(Order, id=228)
    # computers2 = order.computers.all()
    
    # result = request.GET.get('result', None)
    # print("Выбранные компьютеры", result)
    # selected_computers = json.loads(result)
    

    orders = Order.objects.exclude(computers=None)
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
        # selected_order_datetime = datetime.combine(order.day, order.time)
        print(o.time)
        if o.time != None or o.day != None:
            
            order_duration_seconds = int(o.duration) * 60

            order_datetime = datetime.combine(o.day, o.time)
            order_unix_time = order_datetime.timestamp()
            order_total_unix_time = order_unix_time + order_duration_seconds

            # all_computers = order.computers.all()
            computers_titles = [computer.title for computer in computers2]
            # если попали в промежуток, то говорим, какие компы не отображать
            print(order_datetime, selected_datetime, duration, order_datetime, o.duration)
            print(datetime.fromtimestamp(order_unix_time), datetime.fromtimestamp(selected_unix_time), datetime.fromtimestamp(order_total_unix_time))
            print(int(order_unix_time), int(selected_unix_time), int(order_total_unix_time))
                  
            if int(order_unix_time) < int(selected_unix_time) < int(order_total_unix_time):
                
                block_list+=computers_titles

            # print(selected_datetime, selected_order_datetime)
            
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
    
    context = {
        'data': json.dumps (data),
        'services': all_services,
        'day': day,
        'time': time,
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