from django.db import models

class Clase(models.Model):
    clase = models.CharField(max_length=70, verbose_name="clase", null=False, blank=False)
    descripcion = models.CharField(max_length=70, verbose_name="descripcion", null=False, blank=False)
    capacidad_max = models.IntegerField(verbose_name="capacidad_max", default="0")

    