from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from .models import TipoClase, HorarioClase
from datetime import datetime, timedelta
from schedule.models import Calendar, Event
from django.views import View



class TipoClaseCreateView(CreateView):
    model = TipoClase
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('home')


class TipoClaseUpdateView(UpdateView):
    model = TipoClase
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('home')


class ClasesListView(ListView):
    paginate_by = 10
    model = HorarioClase
    template_name = "clases/clase_list.html"
    context_object_name = 'horarios'

    def get_queryset(self):
        dia = self.request.GET.get('dia', '')
        qs = HorarioClase.objects.select_related('tipo_clase').order_by('dia', 'hora')

        if dia:
            qs = qs.filter(dia=dia)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dia'] = self.request.GET.get('dia', '')
        return context

DIAS_MAP = {
    'L': 0,
    'M': 1,
    'X': 2,
    'J': 3,
    'V': 4,
    'S': 5,
    'D': 6,
}


def sincronizar_clases():
    calendario, _ = Calendar.objects.get_or_create(
        name="Calendario Gimnasio",
        slug="calendario-gimnasio"
    )

    hoy = datetime.today()

    horarios = HorarioClase.objects.select_related("tipo_clase")

    for h in horarios:

        dia_objetivo = DIAS_MAP[h.dia]

        dias_ahead = dia_objetivo - hoy.weekday()
        if dias_ahead < 0:
            dias_ahead += 7

        fecha_clase = hoy + timedelta(days=dias_ahead)
        fecha_inicio = timezone.make_aware(datetime.combine(fecha_clase.date(), h.hora)
)

        if not Event.objects.filter(
            title=h.tipo_clase.nombre,
            start=fecha_inicio
        ).exists():

            Event.objects.create(
                calendar=calendario,
                title=h.tipo_clase.nombre,
                start=fecha_inicio,
                end=fecha_inicio + timedelta(hours=1),
            )

class CalendarioView(TemplateView):
    template_name = "portfolio/calendario.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        print("SINCRONIZANDO CLASES")
        sincronizar_clases()

        calendario, _ = Calendar.objects.get_or_create(
            name="Calendario Gimnasio",
            slug = "calendario-gimnasio"
        )

        context["tipos"] = TipoClase.objects.all()
        context["calendario"] = calendario

        return context

class InscribirseClasesView(View):
    def get(self, request):
        return redirect(reverse_lazy('calendario_usuario'))
    
class MisClasesView(TemplateView):
    template_name = "clases/mis_clases.html"
