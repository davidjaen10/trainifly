from django import forms
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

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
    
@method_decorator(staff_member_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['nombre', 'email', 'usuario', 'plan']
    template_name = "users/user_form.html"
    success_url = reverse_lazy('admin_clientes_list')

@method_decorator(staff_member_required, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = "adminpanel/users/confirm_delete.html"
    success_url = reverse_lazy("admin_clientes_list")