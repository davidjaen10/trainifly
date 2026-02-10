from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class MyUserManager(BaseUserManager):
    def create_user(self, email=None, usuario=None, password=None, **extra_fields):
        if not email and not usuario:
            raise ValueError("Debes proporcionar email o usuario")

        if email:
            email = self.normalize_email(email)
        user = self.model(email=email, usuario=usuario, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Ha de proporcionar un e-mail válido")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        extra_fields.setdefault("usuario", "admin")

        return self.create_user(
            email=email,
            password=password,
            **extra_fields
        )

class User(AbstractBaseUser, PermissionsMixin):
    PLANES = [
        ("basico", "Plan Básico - 25€/mes"),
        ("premium", "Plan Premium - 40€/mes"),
        ("elite", "Plan Élite - 60€/mes"),
    ]

    username = None
    nombre = models.CharField(max_length=70)
    usuario = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    dni = models.CharField(max_length=9, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    plan = models.CharField(max_length=20, choices=PLANES, default="basico")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyUserManager()
    USERNAME_FIELD = "usuario"
    REQUIRED_FIELDS = ["email"]
    
    def __str__(self):
        return self.usuario
