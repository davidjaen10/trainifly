from django.shortcuts import render
from django.views.generic import TemplateView, FormView, View
from users.forms import UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from users.models import User

class HomeView(TemplateView):
    template_name = 'portfolio/home.html'

class AdminPortfolioView(TemplateView):
    template_name = "portfolio/admin.html"

class LoginView(FormView):
    template_name = 'portfolio/login.html'
    form_class = UserLoginForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        try:
            user_obj = User.objects.get(usuario=email)
        except User.DoesNotExist:
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                user_obj = None

        if user_obj is None:
            form.add_error(None, "Email o contraseña incorrectos.")
            return self.form_invalid(form)

        user = authenticate(self.request, username=user_obj.usuario, password=password)

        if user is None:
            form.add_error(None, "Email o contraseña incorrectos.")
            return self.form_invalid(form)

        login(self.request, user)

        if user.is_staff or user.is_superuser:
            return redirect("inicio_admin")
        
        return redirect("home")

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")