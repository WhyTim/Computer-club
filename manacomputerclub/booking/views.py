from datetime import datetime
import json
from pyexpat.errors import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
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
        return redirect('booking:success')


    computers = Computers.objects.all().values('id', 'title')
    data = {
        'computers': list(computers),
    }

    result = request.GET.get('result', None)
    # selected_computers = json.loads(result)



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

    return render(request, 'booking/html/bookingComplete.html')