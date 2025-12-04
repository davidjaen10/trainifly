from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Usuario

class HomeView(TemplateView):
    template_name = 'portfolio/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '') #obtener el texto buscado
        if q:
            context["usuarios"] = Usuario.objects.filter(nombre__icontains = q)#.exclude(nombre__iexact="geyzan")
        else:
            #user_pag = 10
            #num_pag = 4
            context['usuarios'] = Usuario.objects.all()#[num_pag:user_pag*num_pag]#devuelve
        marcado_vista = self.request.GET.get('marcado', '')
        if marcado_vista == "True":
            context["usuarios"] = context["usuarios"].filter(edad__lte=10).order_by("nombre")#SI ESTA MARCADO FILTRAR
        context["marcado"] = marcado_vista

        #usuario = Usuario(nombre="pepe".....) para crear un usuario
        #usuario.save() para guardarlo
        context['q'] = q
        return context
    

