from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Cliente, Coche, Servicio, CocheServicio
from django.shortcuts import render

#PRACTICA 3
def lista_clientes(request):
    #clientes = list(Cliente.objects.values("id", "nombre", "telefono", "email"))
    #return JsonResponse(clientes, safe=False)
    clientes = Cliente.objects.all()
    return render(request, 'app_gestion_coches/lista_clientes.html', {'clientes': clientes})


def detalle_cliente(request, cliente_id):
    #try:
    #    cliente = Cliente.objects.values("id", "nombre", "telefono", "email").get(id=cliente_id)
    #    return JsonResponse(cliente)
    #except Cliente.DoesNotExist:
    #    return JsonResponse({"error": "Cliente no encontrado"}, status=404)
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        coches = Coche.objects.filter(cliente=cliente)
        contexto = {
            'cliente': cliente,
            'coches': coches,
        }
        return render(request, 'app_gestion_coches/detalle_cliente.html', contexto)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)


#PRACTICA 4
@csrf_exempt
def registrar_cliente(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.create(
                nombre=data['nombre'],
                telefono=data['telefono'],
                email=data['email']
            )
            return JsonResponse({"mensaje": "Cliente registrado con éxito", "cliente_id": cliente.id})
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def registrar_coche(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.get(id=data['cliente_id'])
            coche = Coche.objects.create(
                cliente=cliente,
                marca=data['marca'],
                modelo=data['modelo'],
                matricula=data['matricula']
            )
            return JsonResponse({"mensaje": "Coche registrado con éxito", "coche_id": coche.id})
        except Cliente.DoesNotExist:
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def registrar_servicio(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            coche = Coche.objects.get(id=data['coche_id'])
            servicio = Servicio.objects.create(
                nombre=data['nombre'],
                descripcion=data['descripcion']
            )
            CocheServicio.objects.create(coche=coche, servicio=servicio)
            return JsonResponse({"mensaje": "Servicio registrado con éxito", "servicio_id": servicio.id})
        except Coche.DoesNotExist:
            return JsonResponse({"error": "Coche no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

#BUSCAR CLIENTE SE HIZO EN LA PRACTICA 3 (detalle_cliente)

@csrf_exempt
def buscar_coche_por_matricula(request, matricula):
    #try:
    #    coche = Coche.objects.get(matricula=matricula)
    #    respuesta = {
    #        "coche": {
    #            "id": coche.id,
    #            "marca": coche.marca,
    #            "modelo": coche.modelo,
    #            "matricula": coche.matricula
    #        }
    #    }
    #    return JsonResponse(respuesta)
    #except Coche.DoesNotExist:
    #    return JsonResponse({"error": "Coche no encontrado"}, status=404)
    try:
        coche = Coche.objects.get(matricula=matricula)
        contexto = {
            'coche': coche
        }
        return render(request, 'app_gestion_coches/detalle_coche.html', contexto)
    except Coche.DoesNotExist:
        return JsonResponse({"error": "Coche no encontrado"}, status=404)

@csrf_exempt
def buscar_coches_de_cliente(request, cliente_id):
    #try:
    #    coches = list(Coche.objects.filter(cliente_id=cliente_id).values("id", "marca", "modelo", "matricula"))
    #    return JsonResponse(coches, safe=False)
    #except Cliente.DoesNotExist:
    #    return JsonResponse({"error": "Cliente no encontrado"}, status=404)
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        coches = Coche.objects.filter(cliente=cliente)
        contexto = {
            'cliente': cliente,
            'coches': coches
        }
        return render(request, 'app_gestion_coches/coches_cliente.html', contexto)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Coche no encontrado"}, status=404)

@csrf_exempt
def buscar_servicio(request, servicio_id):
    #try:
    #    servicio = Servicio.objects.values("id", "nombre", "coches", "descripcion").get(id=servicio_id)
    #    return JsonResponse(servicio)
    #except Servicio.DoesNotExist:
    #    return JsonResponse({"error": "Servicio no encontrado"}, status=404)
    try:
        servicio = Servicio.objects.get(id=servicio_id)
        # Si quieres mostrar qué coches tienen este servicio:
        coches_con_servicio = servicio.coches.all() 
        contexto = {
            'servicio': servicio,
            'coches': coches_con_servicio
        }
        return render(request, 'app_gestion_coches/detalle_servicio.html', contexto)
    except Servicio.DoesNotExist:
        return JsonResponse({"error": "Servicio no encontrado"}, status=404)

@csrf_exempt
def servicios_coche(request, coche_id):
    #try:
    #    servicios = list(Servicio.objects.filter(coches__id=coche_id).values("id", "nombre", "descripcion"))
    #    return JsonResponse(servicios, safe=False)
    #except Exception as e:
    #    return JsonResponse({"error": str(e)}, status=500)
    try:
        coche = Coche.objects.get(id=coche_id)
        coche_servicios = CocheServicio.objects.filter(coche=coche).select_related('servicio')
        contexto = {
            'coche': coche,
            'coche_servicios': coche_servicios,
        }
        return render(request, 'app_gestion_coches/servicios_coche.html', contexto)
    except Coche.DoesNotExist:
        return JsonResponse({"error": "Coche no encontrado"}, status=404)

    
@csrf_exempt
def buscar_cliente_por_nombre(request, nombre):
    #try: 
    #    cliente = Cliente.objects.get(nombre=nombre)
    #    respuesta = {
    #        "id": cliente.id,
    #        "nombre": cliente.nombre,
    #        "telefono": cliente.telefono,
    #        "email": cliente.email
    #    }
    #    return JsonResponse(respuesta)
    #except Cliente.DoesNotExist:
    #    return JsonResponse({"error": "Cliente no encontrado"}, status=404)
    try: 
        cliente = Cliente.objects.get(nombre=nombre)
        contexto = {
            'cliente': cliente
        }
        return render(request, 'app_gestion_coches/detalle_cliente_nombre.html', contexto)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)

#PRACTICA 5
def inicio(request):
    contexto = {'mensaje': '¡Bienvenido a mi sitio web!'}
    return render(request, 'inicio.html', contexto)

def acerca_de(request):
    return render(request, 'acerca.html', {'nombre': 'Bruno Egido'})
