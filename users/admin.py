from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = list_display_links = ("nombre", "usuario", "email", "tipo")
    search_fields = ["nombre", "usuario", "email", "tipo"]
    def save_model(self, request, obj, form, change):
        if not change or 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)



admin.site.register(User, UserAdmin)