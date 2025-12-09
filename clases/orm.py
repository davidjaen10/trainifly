from django.shortcuts import render
from models import Clase

def filtrar_clases_por_dia(request):
    dia = request.GET.get('dia')
    clases = Clase.objects.filter(dia = dia) if dia else []
    return render(request, 'clase_list.html', {'clases': clases, 'dia': dia})