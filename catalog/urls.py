from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('buscar/', views.search, name='search'),
    path('proveedores/<int:pk>/', views.provider_detail, name='provider_detail'),
    path('panel/', views.provider_dashboard, name='dashboard'),
    path('panel/perfil/', views.profile_edit, name='profile_edit'),
    path('panel/servicios/nuevo/', views.service_form, name='service_new'),
    path('panel/servicios/<int:pk>/editar/', views.service_form, name='service_edit'),
    path('panel/servicios/<int:pk>/activar/', views.service_toggle, name='service_toggle'),
]
