from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class MyUserManager(BaseUserManager):
    def create_user(
        self, email, first_name=None, last_name=None, password=None, type=None
    ):
        """
        Crea y guarda un usuario con el email y la contraseña.
        """
        if not email:
            raise ValueError("Ha de proporcionar un e-mail válido")

        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name,)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Crea y guarda un SuperUsuario con el email y la contraseña.
        """
        if not email:
            raise ValueError("Ha de proporcionar un e-mail válido")

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)
    activo = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    # Campos de Usuario
    nombre = models.CharField(max_length=70, default="Admin")
    usuario = models.CharField(max_length=50, unique=True, default="admin")
    tipo_usuarios = models.TextChoices("tipo_usuario", "Usuario Profesor")
    tipo = models.CharField(max_length=20, choices=tipo_usuarios, default="Usuario")
    edad = models.IntegerField(default=18)
    fecha_inscripcion = models.DateTimeField(default=now)
    imagen_perfil = models.ImageField(null=True, blank=True)

    objects = MyUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

