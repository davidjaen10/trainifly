from django import forms
from clases.models import Clase
from users.models import Usuario

class ClaseAdminForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = '__all__'

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'