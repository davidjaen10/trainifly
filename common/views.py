from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from users.forms import UserLoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

class HomeView(TemplateView):
    template_name = 'portfolio/home.html'

class LoginView(FormView):
    template_name = 'portfolio/login.html'
    form_class = UserLoginForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        user = authenticate(self.request, email=email, password=password)

        if user is None:
            form.add_error(None, "Email o contraseña incorrectos.")
            return self.form_invalid(form)

        login(self.request, user)
        return redirect("home")