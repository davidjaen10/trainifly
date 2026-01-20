from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'portfolio/home.html'

class LoginView(TemplateView):
    template_name = 'portfolio/login.html'