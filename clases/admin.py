# from django.contrib import admin
# from .models import Clase

# class ClaseAdmin(admin.ModelAdmin):
#     list_display = list_display_links = ("clase", "descripcion")
#     search_fields = ["clase", "descripcion"]



# admin.site.register(Clase, ClaseAdmin)

from django.contrib import admin
from .models import TipoClase, HorarioClase


@admin.register(TipoClase)
class TipoClaseAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)


@admin.register(HorarioClase)
class HorarioClaseAdmin(admin.ModelAdmin):
    list_display = ("tipo_clase", "dia", "hora", "capacidad_max")
    list_filter = ("dia", "tipo_clase")
