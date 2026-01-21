from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("nombre", "usuario", "email", "is_staff", "is_active", "plan")
    list_display_links = ("nombre",)
    search_fields = ("nombre", "usuario", "email", "dni")
    ordering = ("email",)


admin.site.register(User, UserAdmin)