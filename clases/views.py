from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from .models import TipoClase, HorarioClase
from schedule.periods import Month
from collections import defaultdict
from datetime import datetime, timedelta, date
from schedule.models import Calendar, Event
from django.views import View
#
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class protegido(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class TipoClaseCreateView(CreateView, protegido):
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
    dias_futuro = 60

    horarios = HorarioClase.objects.select_related("tipo_clase")

    for h in horarios:

        dia_objetivo = DIAS_MAP[h.dia]

        for i in range(dias_futuro):

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
                        description=f"tipo:{h.tipo_clase.id}",
                        start=fecha_inicio,
                        end=fecha_inicio + timedelta(hours=1),
                    )


from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from .models import TipoClase, HorarioClase
from schedule.periods import Month
from collections import defaultdict
from datetime import datetime, timedelta, date
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

    hoy = date.today()
    dias_futuro = 60

    horarios = HorarioClase.objects.select_related("tipo_clase")

    for h in horarios:

        dia_objetivo = DIAS_MAP[h.dia]

        for i in range(dias_futuro):

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
                        description=f"tipo:{h.tipo_clase.id}",
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

            if year < today.year or (year == today.year and month < today.month):
                year = today.year
                month = today.month
        else:
            year = today.year
            month = today.month

        period = Month(calendario.events.all(), date(year, month, 1))

        tipo_id = self.request.GET.get("tipo")

        if tipo_id:
            tipo = TipoClase.objects.get(id=tipo_id)
            eventos = calendario.events.filter(
                description=f"tipo:{tipo.id}"
            )
        else:
            eventos = calendario.events.all()

        context["calendar"] = calendario
        context["period"] = period
        context["tipos"] = TipoClase.objects.all()
        context["tipo_activo"] = tipo_id
        context["now"] = today

        return context
    
class InscribirseClasesView(View):
    def get(self, request):
        return redirect(reverse_lazy('calendario_usuario'))
    
class MisClasesView(TemplateView):
    template_name = "clases/mis_clases.html"

class InscribirseClasesView(View):
    def get(self, request):
        return redirect(reverse_lazy('calendario_usuario'))
    
class MisClasesView(TemplateView):
    template_name = "clases/mis_clases.html"
