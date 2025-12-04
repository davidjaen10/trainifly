from django.contrib import admin
from .models import Clase

class ClaseAdmin(admin.ModelAdmin):
    list_display = list_display_links = ("clase", "descripcion")
    search_fields = ["clase", "descripcion"]



admin.site.register(Clase, ClaseAdmin)