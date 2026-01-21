from django import forms
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import CreateView

from .models import User

class UserRegisterForm(forms.ModelForm):
    PLANES = [
        ("basico", "Plan Básico - 25€/mes"),
        ("premium", "Plan Premium - 40€/mes"),
        ("elite", "Plan Élite - 60€/mes"),
    ]

    plan = forms.ChoiceField(choices=PLANES, required=True)

    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repite contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["nombre", "usuario", "email", "dni", "fecha_nacimiento", "plan"]

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")

        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")

        return cleaned


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.set_password(form.cleaned_data["password1"])
        user.save()
        
        login(self.request, user,  backend="django.contrib.auth.backends.ModelBackend")
        return super().form_valid(form)
