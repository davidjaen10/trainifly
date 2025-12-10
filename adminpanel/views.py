from django.shortcuts import render
from django.views.generic import ListView
from clases.models import Clase

class AdminListView(ListView):
    paginate_by = 20
    model = Clase
    template_name = "adminpanel/clases.html"
    context_object_name = 'clases'

    def get_queryset(self):
        dia = self.request.GET.get('dia', '')
        qs = Clase.objects.all().order_by('dia', 'hora')
        if dia:
            qs = qs.filter(dia=dia)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dia'] = self.request.GET.get('dia', '')
        return context
        