from django.urls import path
from . import views

app_name = "booking"  

urlpatterns = [
    path('', views.index, name='order'),
    path('submit/', views.bookingSubmit, name='submit'),
    path('successful/', views.bookingSuccess, name='success'),

]
