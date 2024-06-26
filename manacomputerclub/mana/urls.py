from django.urls import path
from . import views

# app_name = "mana"  # для urls основного

urlpatterns = [
    path('', views.index, name='home'),
    path('services', views.services, name='services'),
    path('news', views.news, name='news'),
    path('about', views.about, name='about'),
    path('account', views.account, name='account'),
    path('news/<int:news_id>/', views.newsid, name='news_id'),
    path('account/delete/<int:order_id>/', views.delete_order, name='delete_order'),
]
