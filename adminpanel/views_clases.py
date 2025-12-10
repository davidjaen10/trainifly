from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from clases.models import Clase
from .forms import ClaseAdminForm

def clases_list(request):
    clases = Clase.objects.all()
    return render(request, 'adminpanel/clases/list.html', {'clases': clases})

def clases_create(request):
    if request.method == "POST":
        form = ClaseAdminForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Clase creada')
            return redirect('admin_clases_list')
        else:
            form = ClaseAdminForm()
    return render(request, 'adminpanel/clases/form.html', {'form': form, 'modo': 'Crear'})

def clases_edit(request, id):
    clase = get_object_or_404(Clase, id = id)
    if request.method == 'POST':
        form = ClaseAdminForm(request.POST, instance = clase)
        if form.is_valid():
            form.save()
            messages.succes(request, 'Clase actualizada')
            return redirect('admin_clases_list')
    else:
        form = ClaseAdminForm(instance=clase)
    return render(request, 'adminpanel/clases/form.html', {'form': form, 'modo': 'Editar'})

def clases_delete(request, id):
    clase = get_object_or_404(Clase, id=id)

    if request.method == 'POST':
        clase.delete()
        messages.success(request, 'Clase eliminada')
        return redirect('admin_clases_list')

    return render(request, 'adminpanel/clases/confirm_delete.html', {'clase': clase})