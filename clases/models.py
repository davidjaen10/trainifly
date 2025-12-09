from django.db import models
from datetime import datetime

DIAS_SEMANA = [
    ('L', 'Lunes'),
    ('M', 'Martes'),
    ('X', 'Miércoles'),
    ('J', 'Jueves'),
    ('V', 'Viernes'),
    ('S', 'Sábado'),
    ('D', 'Domingo'),
]

class Clase(models.Model):
    clase = models.CharField(max_length=70, verbose_name="clase", null=False, blank=False)
    descripcion = models.CharField(max_length=70, verbose_name="descripcion", null=False, blank=False)
    dia = models.CharField(max_length=1, choices=DIAS_SEMANA, default = "L")
    hora = models.TimeField(default =datetime.now )
    capacidad_max = models.IntegerField(verbose_name="capacidad_max", default="0")

    