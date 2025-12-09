from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from .models import Clase

class UserCreateView(CreateView):
    model = Clase
    fields = ['clase', "descripcion"]
    success_url = reverse_lazy('home')

class UserUpdateView(UpdateView):
    model = Clase
    fields = ['clase', 'descripcion']
    success_url = reverse_lazy('home')

class clasesListView(ListView):
    paginate_by = 10
    model = Clase
    template_name = "clases/clase_list.html"
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
