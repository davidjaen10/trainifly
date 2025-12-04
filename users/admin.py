from django.contrib import admin
from .models import Usuario

class UserAdmin(admin.ModelAdmin):
    list_display = list_display_links = ("nombre", "usuario", "email", "tipo")
    search_fields = ["nombre", "usuario", "email", "tipo"]



admin.site.register(Usuario, UserAdmin)