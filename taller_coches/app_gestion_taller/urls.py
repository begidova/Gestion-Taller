from django.urls import path
from . import views
from .views import (lista_clientes, detalle_cliente,
                    registrar_cliente, registrar_coche, registrar_servicio,
                    buscar_coche_por_matricula, buscar_coches_de_cliente, buscar_servicio, servicios_coche, buscar_cliente_por_nombre,
                    nuevo_cliente, lista_coches, lista_coches_servicios, lista_servicios, nuevo_coche, nuevo_coche_servicio, nuevo_servicio, editar_cliente, editar_coche, editar_coche_servicio, editar_servicio, eliminar_cliente, eliminar_coche, eliminar_coche_servicio, eliminar_servicio)

urlpatterns = [
    # RACTICA 6
    path('clientes/nuevo/', nuevo_cliente, name='nuevo_cliente'),
    path('coches/nuevo/', nuevo_coche, name='nuevo_coche'),
    path('servicios/nuevo/', nuevo_servicio, name='nuevo_servicio'),
    path('coches-servicios/nuevo/', nuevo_coche_servicio, name='nuevo_coche_servicio'),
    path('coches/', lista_coches, name='lista_coches'),
    path('servicios/', lista_servicios, name='lista_servicios'),
    path('coches-servicios/', lista_coches_servicios, name='lista_coches_servicios'),
    path('coches/editar/<int:coche_id>/', editar_coche, name='editar_coche'),
    path('clientes/editar/<int:cliente_id>/', editar_cliente, name='editar_cliente'),
    path('servicios/editar/<int:servicio_id>/', editar_servicio, name='editar_servicio'),
    path('coches-servicios/editar/<int:coche_servicio_id>/', editar_coche_servicio, name='editar_coche_servicio'),
    path('coches/eliminar/<int:coche_id>/', eliminar_coche, name='eliminar_coche'),
    path('clientes/eliminar/<int:cliente_id>/', eliminar_cliente, name='eliminar_cliente'),
    path('servicios/eliminar/<int:servicio_id>/', eliminar_servicio, name='eliminar_servicio'),
    path('coches-servicios/eliminar/<int:coche_servicio_id>/', eliminar_coche_servicio, name='eliminar_coche_servicio'),

    
    # PRACTICA 3
    path('clientes/', lista_clientes, name='lista_clientes'),
    path('clientes/<int:cliente_id>/', detalle_cliente, name='detalle_cliente'),


    # PRACTICA 4
    path('clientes/registrar/', registrar_cliente, name='registrar_cliente'),
    path('coches/registrar/', registrar_coche, name='registrar_coche'),
    path('servicios/registrar/', registrar_servicio, name='registrar_servicio'),

    path('coches/<str:matricula>/', buscar_coche_por_matricula, name='buscar_coche_por_matricula'),
    path('clientes/<int:cliente_id>/coches/', buscar_coches_de_cliente, name='buscar_coches_de_cliente'),
    path('servicios/<int:servicio_id>/', buscar_servicio, name='buscar_servicio'),
    path('coches/<int:coche_id>/servicios/', servicios_coche, name='servicios_coche'),
    path('clientes/<str:nombre>/', buscar_cliente_por_nombre, name='buscar_cliente_por_nombre'),
    

    # PRACTICA 5
    path('', views.inicio, name='inicio'),
    path('acerca/', views.acerca_de, name='acerca'),

]
