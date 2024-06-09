from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomAuthenticationForm, RegisterUserForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect


class LoginUser(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/signin.html'
    extra_context = {'title': 'Авторизация'}


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/signup.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')
    # return render(request, 'users/signup.html')
