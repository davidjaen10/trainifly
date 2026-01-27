from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from users.models import User
from .forms import UserAdminForm
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def users_list(request):
    usuarios = User.objects.all()
    return render(request, 'adminpanel/users/list.html', {'usuarios': usuarios})

@staff_member_required
def users_create(request):
    if request.method == 'POST':
        form = UserAdminForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('admin_users_list')
    else:
        form = UserAdminForm()

    return render(request, 'adminpanel/users/form.html', {'form': form, 'modo': 'Crear'})

@staff_member_required
def users_edit(request, id):
    usuario = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UserAdminForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('admin_users_list')
    else:
        form = UserAdminForm(instance=usuario)

    return render(request, 'adminpanel/users/form.html', {'form': form, 'modo': 'Editar'})

@staff_member_required
def users_delete(request, id):
    usuario = get_object_or_404(User, id=id)

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('admin_users_list')

    return render(request, 'adminpanel/users/confirm_delete.html', {'usuario': usuario})
