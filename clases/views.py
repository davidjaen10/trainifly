from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from .models import TipoClase, HorarioClase


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
