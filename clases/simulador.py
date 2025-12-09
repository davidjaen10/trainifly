from faker import Faker
from .models import Clase
from datetime import time
import random


fake = Faker("es_ES")
DIAS_SEMANA = ['L', 'M', 'X', 'J', 'V', 'S', 'D']


def crear_clases(n):
    for x in range(n):
        Clase.objects.create(
            clase = fake.name()[:10],
            descripcion = fake.sentence()[:20],
            dia = random.choice(DIAS_SEMANA),
            hora = time(random.randint(8, 20), random.choice([0, 15, 30, 45])),
            capacidad_max = random.randint(5, 30)
        )

