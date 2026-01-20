from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, Submit
from django.contrib.auth.hashers import check_password
from .models import User

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Contraseña"
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"

        self.helper.layout = Layout(
            Fieldset(
                "Iniciar sesión",
                Row(
                    Column("email", css_class="col-md-6"),
                    Column("password", css_class="col-md-6")
                )
            ),
            Submit("submit", "Iniciar Sesión", css_class="btn btn-primary")
        )

    def clean(self):
        """
        Esto valida usuario/password.
        OJO: esto NO inicia sesión, solo valida.
        El login real lo hace la View.
        """
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not (email and password):
            return cleaned_data

        try:
            user = User.objects.get(email=email)

            # usuario inactivo
            if not user.is_active:
                raise forms.ValidationError("Este usuario está inactivo.")

            if not check_password(password, user.password):
                raise forms.ValidationError("Email o contraseña incorrectos.")

        except User.DoesNotExist:
            raise forms.ValidationError("Email o contraseña incorrectos.")

        return cleaned_data