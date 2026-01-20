from django.shortcuts import render
from django import forms
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import CreateView
from .models import User

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repite contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "nombre", "edad"]  # NO ponemos password aquí

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")

        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")

        return cleaned

class UserCreateView(CreateView):
    model = User
    form_class =UserRegisterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save(commit=False)

        # activamos el user
        user.is_active = True

        # para el hash de la contraseña
        user.set_password(form.cleaned_data["password"])
        user.save()

        # Para iniciar sesion automaticamente
        login(self.request, user)

        return super().form_valid(form)