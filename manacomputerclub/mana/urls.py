from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('news/<int:news_id>/', views.news, name='news'),
    path('news/<slug:news_slug>/', views.news_slug, name='news'),
]
