from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
    path('', views.index, name='order'),
    path('submit/', views.booking_submit, name='submit'),
    path('successful/', views.booking_success, name='success'),
    path('get_available_computers/', views.get_available_computers, name='get_available_computers'),
]
