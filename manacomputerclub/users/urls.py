from django.urls import path
from . import views

app_name = "users"  # для urls основного

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
]