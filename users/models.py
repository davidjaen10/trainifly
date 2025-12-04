from django.db import models
from django.utils.timezone import now


class Usuario(models.Model):
    nombre = models.CharField(max_length=70, verbose_name="nombre", null=False, blank=False)
    usuario = models.CharField(max_length=50, verbose_name="usuario", null=False, blank=False, unique=True)
    email = models.EmailField(max_length=100, verbose_name="email", null=False, blank=False, unique=True)
    passw = models.CharField(max_length=80, verbose_name="passw", null=False, blank=False)

    tipo_usuarios = models.TextChoices("tipo_usuario", "Usuario Profesor")
    tipo = models.CharField(max_length=20, blank=False, verbose_name = "tipo_usuario", choices = tipo_usuarios, default="")

    edad = models.IntegerField(verbose_name="edad")
    fecha_inscripcion = models.DateTimeField(verbose_name='fecha inscripcion', default=now)
    imagen_perfil = models.ImageField(verbose_name = 'imagen', null=True, blank=True)