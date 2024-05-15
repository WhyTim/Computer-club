from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/signin.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('login')
# def login(request):
#     # return render(request, 'users/signup.html')
#     return HttpResponse("login")


def register(request):
    # return render(request, 'users/signup.html')
    return HttpResponse("register")


def logout_user(request):
    return HttpResponse("logout")
