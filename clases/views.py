from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView
from .models import Clase

class UserCreateView(CreateView):
    model = Clase
    fields = ['clase', "descripcion"]
    success_url = reverse_lazy('home')

class UserUpdateView(UpdateView):
    model = Clase
    fields = ['clase', 'descripcion']
    success_url = reverse_lazy('home')