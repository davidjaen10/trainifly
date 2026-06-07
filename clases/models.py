# from django.db import models
# from datetime import datetime

# DIAS_SEMANA = [
#     ('L', 'Lunes'),
#     ('M', 'Martes'),
#     ('X', 'Miércoles'),
#     ('J', 'Jueves'),
#     ('V', 'Viernes'),
#     ('S', 'Sábado'),
#     ('D', 'Domingo'),
# ]

# class Clase(models.Model):
#     clase = models.CharField(max_length=70, verbose_name="clase", null=False, blank=False)
#     descripcion = models.CharField(max_length=70, verbose_name="descripcion", null=False, blank=False)
#     dia = models.CharField(max_length=1, choices=DIAS_SEMANA, default = "L")
#     hora = models.TimeField(default =datetime.now )
#     capacidad_max = models.IntegerField(verbose_name="capacidad_max", default="0")

from django.db import models


class TipoClase(models.Model):
    nombre = models.CharField(max_length=70, unique=True, verbose_name="Nombre de la clase")
    descripcion = models.CharField(max_length=150, verbose_name="Descripción")

    class Meta:
        verbose_name = "Tipo de clase"
        verbose_name_plural = "Tipos de clases"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class HorarioClase(models.Model):
    DIAS_SEMANA = [
        ('L', 'Lunes'),
        ('M', 'Martes'),
        ('X', 'Miércoles'),
        ('J', 'Jueves'),
        ('V', 'Viernes'),
        ('S', 'Sábado'),
        ('D', 'Domingo'),
    ]

    tipo_clase = models.ForeignKey(
        TipoClase,
        on_delete=models.CASCADE,
        related_name="horarios",
        verbose_name="Tipo de clase"
    )
    dia = models.CharField(max_length=1, choices=DIAS_SEMANA, verbose_name="Día")
    hora = models.TimeField(verbose_name="Hora")
    capacidad_max = models.PositiveIntegerField(default=0, verbose_name="Capacidad máxima")

    class Meta:
        verbose_name = "Horario de clase"
        verbose_name_plural = "Horarios de clases"
        ordering = ["dia", "hora"]
        unique_together = ("tipo_clase", "dia", "hora")  # Evita duplicados

    def __str__(self):
        return f"{self.tipo_clase.nombre} - {self.get_dia_display()} {self.hora.strftime('%H:%M')}"
