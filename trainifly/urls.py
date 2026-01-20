"""
URL configuration for trainifly project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views
from clases import views as views2
from clases import views as views3
from django.conf.urls.static import static
from django.conf import settings
from adminpanel import views_clases, views_users
from common import views as viewcommon

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name= 'home'),
    path('create/', view = views2.UserCreateView.as_view(), name='crear' ),
    path('clases_actualizar/<int:pk>', view= views2.UserUpdateView.as_view(), name="actualizar"),
    path('listado_clases/', view = views3.clasesListView.as_view(), name = 'listado'),
    path('adminpanel/clases/', views_clases.clases_list, name='admin_clases_list'),
    path('adminpanel/clases/nueva/', views_clases.clases_create, name='admin_clases_create'),
    path('adminpanel/clases/<int:id>/editar/', views_clases.clases_edit, name='admin_clases_edit'),
    path('adminpanel/clases/<int:id>/eliminar/', views_clases.clases_delete, name='admin_clases_delete'),
    path('adminpanel/usuarios/', views_users.users_list, name='admin_users_list'),
    path('adminpanel/usuarios/nuevo/', views_users.users_create, name='admin_users_create'),
    path('adminpanel/usuarios/<int:id>/editar/', views_users.users_edit, name='admin_users_edit'),
    path('adminpanel/usuarios/<int:id>/eliminar/', views_users.users_delete, name='admin_users_delete'),
    path('accounts/', include('allauth.urls')),
    path('login/', view = viewcommon.LoginView.as_view(), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
