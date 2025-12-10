from faker import Faker
from .models import Usuario
import random
from django.utils import timezone
from datetime import timedelta

fake = Faker("es_ES")
TIPO_USUARIOS = ["Usuario", "Profesor"]

def crear_usuarios(n):
    now = timezone.now()
    for _ in range(n):
        # Generar un datetime aleatorio en los últimos 5 años como aware
        fecha_aware = now - timedelta(days=random.randint(0, 5*365), 
                                     seconds=random.randint(0, 86400))

        Usuario.objects.create(
            nombre=fake.name()[:70],
            usuario=fake.unique.user_name()[:50],
            email=fake.unique.email()[:100],
            passw=fake.password(length=10),
            tipo=random.choice(TIPO_USUARIOS),
            edad=random.randint(18, 80),
            fecha_inscripcion=fecha_aware,  # Aware datetime garantizado
            imagen_perfil=None
        )
