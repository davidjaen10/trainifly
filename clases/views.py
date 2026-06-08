from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from .models import TipoClase, HorarioClase, ReservaClase
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView
from django.views import View
from schedule.periods import Month
from schedule.models import Calendar, Event
from datetime import datetime, timedelta, date

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
    hoy = date.today()
    horarios = HorarioClase.objects.select_related("tipo_clase")

    for h in horarios:
        dia_objetivo = DIAS_MAP[h.dia]
        for i in range(60):
            fecha = hoy + timedelta(days=i)
            if fecha.weekday() == dia_objetivo:
                fecha_inicio = timezone.make_aware(
                    datetime.combine(fecha, h.hora)
                )
                if not Event.objects.filter(
                    calendar=calendario,
                    start=fecha_inicio
                ).exists():
                    Event.objects.create(
                        calendar=calendario,
                        title=h.tipo_clase.nombre,
                        description=f"horario:{h.id}",
                        start=fecha_inicio,
                        end=fecha_inicio + timedelta(hours=1),
                    )

class CalendarioView(TemplateView):
    template_name = "portfolio/calendario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sincronizar_clases()

        calendario, _ = Calendar.objects.get_or_create(
            name="Calendario Gimnasio",
            slug="calendario-gimnasio"
        )

        today = date.today()

        year = self.request.GET.get("year")
        month = self.request.GET.get("month")

        if year and month:
            year = int(year)
            month = int(month)
        else:
            year = today.year
            month = today.month

        period = Month(
            calendario.events.all(),
            date(year, month, 1)
        )

        tipo_id = self.request.GET.get("tipo")

        context["calendar"] = calendario
        context["period"] = period
        context["tipos"] = TipoClase.objects.all()
        context["tipo_activo"] = tipo_id
        context["now"] = today
        context["eventos"] = calendario.events.order_by("start")[:20]

        ocupacion = {}
        capacidades = {}
        info_eventos = {}

        for evento in calendario.events.all():

            reservas = evento.reservas.count()
            ocupacion[evento.id] = reservas

            if evento.description.startswith("horario:"):

                horario_id = int(
                    evento.description.replace("horario:", "")
                )

                try:
                    horario = HorarioClase.objects.get(id=horario_id)

                    capacidades[evento.id] = horario.capacidad_max

                    info_eventos[evento.id] = {
                        "ocupadas": reservas,
                        "capacidad": horario.capacidad_max,
                    }

                except HorarioClase.DoesNotExist:
                    capacidades[evento.id] = 0

        context["ocupacion"] = ocupacion
        context["capacidades"] = capacidades
        context["info_eventos"] = info_eventos

        context["eventos_reservados"] = list(
            ReservaClase.objects.filter(
                usuario=self.request.user
            ).values_list("evento_id", flat=True)
        )

        mes_siguiente = (
            today.replace(day=28) + timedelta(days=4)
        ).replace(day=1)

        context["mes_siguiente"] = mes_siguiente

        return context
    
class InscribirseClasesView(View):
    def get(self, request):
        return redirect(reverse_lazy('calendario_usuario'))


class MisClasesView(TemplateView):
    template_name = "clases/mis_clases.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reservas"] = ReservaClase.objects.filter(
            usuario=self.request.user
        ).select_related("evento")
        return context

class ReservarClaseView(View):
    def get(self, request, event_id):
        evento = Event.objects.get(id=event_id)
        ReservaClase.objects.get_or_create(
            usuario=request.user,
            evento=evento
        )
        return redirect("mis_clases")
    
class CancelarReservaView(View):
    def get(self, request, reserva_id):

        ReservaClase.objects.filter(
            id=reserva_id,
            usuario=request.user
        ).delete()

        return redirect("mis_clases")