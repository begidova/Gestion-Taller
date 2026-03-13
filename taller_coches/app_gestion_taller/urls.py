from django.urls import path
from . import views
from .views import (lista_clientes, detalle_cliente, 
                    registrar_cliente, registrar_coche, registrar_servicio,
                    buscar_coche_por_matricula, buscar_coches_de_cliente, buscar_servicio, servicios_coche, buscar_cliente_por_nombre)

urlpatterns = [
    # PRACTICA 3
    path('clientes/', lista_clientes, name='lista_clientes'),
    path('clientes/<int:cliente_id>/', detalle_cliente, name='detalle_cliente'),

    #PRACTICA 4
    path('clientes/registrar/', registrar_cliente, name='registrar_cliente'),
    path('coches/registrar/', registrar_coche, name='registrar_coche'),
    path('servicios/registrar/', registrar_servicio, name='registrar_servicio'),

    path('coches/<str:matricula>/', buscar_coche_por_matricula, name='buscar_coche_por_matricula'),
    path('clientes/<int:cliente_id>/coches/', buscar_coches_de_cliente, name='buscar_coches_de_cliente'),
    path('servicios/<int:servicio_id>/', buscar_servicio, name='buscar_servicio'),
    path('coches/<int:coche_id>/servicios/', servicios_coche, name='servicios_coche'),
    path('clientes/<str:nombre>/', buscar_cliente_por_nombre, name='buscar_cliente_por_nombre'),
    
    #PRACTICA 5
    path('', views.inicio, name='inicio'),
    path('acerca/', views.acerca_de, name='acerca'),
]
