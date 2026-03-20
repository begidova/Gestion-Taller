from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Cliente, Coche, Servicio, CocheServicio
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ClienteForm, CocheForm, ServicioForm, CocheServicioForm

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


#PRACTICA 6
def nuevo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'app_gestion_coches/formulario.html', {'form': form, 'titulo': 'Nuevo Cliente'})

def nuevo_coche(request):
    if request.method == 'POST':
        form = CocheForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_coches')
    else:
        form = CocheForm()
    return render(request, 'app_gestion_coches/formulario.html', {'form': form, 'titulo': 'Nuevo Coche'})

def nuevo_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_servicios')
    else:
        form = ServicioForm()
    return render(request, 'app_gestion_coches/formulario.html', {'form': form, 'titulo': 'Nuevo Servicio'})

def nuevo_coche_servicio(request):
    if request.method == 'POST':
        form = CocheServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_coches_servicios')
    else:
        form = CocheServicioForm()
    return render(request, 'app_gestion_coches/formulario.html', {'form': form, 'titulo': 'Nuevo Servicio de Coche'})

def lista_coches(request):
    coches = Coche.objects.all()
    return render(request, 'app_gestion_coches/lista_coches.html', {'coches': coches})

def lista_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'app_gestion_coches/lista_servicios.html', {'servicios': servicios})

def lista_coches_servicios(request):
    cochesServicios = CocheServicio.objects.all()
    return render(request, 'app_gestion_coches/lista_coches_servicios.html', {'cochesServicios': cochesServicios})

def editar_coche(request, coche_id):
    coche = get_object_or_404(Coche, id=coche_id)
    if request.method == 'POST':
        form = CocheForm(request.POST, instance=coche)
        if form.is_valid():
            form.save()
            return redirect('lista_coches')
    else:
        form = CocheForm(instance=coche)
    
    return render(request, 'app_gestion_coches/formulario.html', {
        'form': form, 
        'titulo': 'Editar Coche: ' + coche.matricula
    })

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'app_gestion_coches/formulario.html', {
        'form': form, 
        'titulo': 'Editar Cliente: ' + cliente.nombre
    })

def editar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('lista_servicios')
    else:
        form = ServicioForm(instance=servicio)
    
    return render(request, 'app_gestion_coches/formulario.html', {
        'form': form, 
        'titulo': 'Editar Servicio: ' + servicio.nombre
    })

def editar_coche_servicio(request, coche_servicio_id):
    servicioCoche = get_object_or_404(CocheServicio, id=coche_servicio_id)
    if request.method == 'POST':
        form = CocheServicioForm(request.POST, instance=servicioCoche)
        if form.is_valid():
            form.save()
            return redirect('lista_coches_servicios')
    else:
        form = CocheServicioForm(instance=servicioCoche)
    
    return render(request, 'app_gestion_coches/formulario.html', {
        'form': form, 
        'titulo': 'Editar Servicio de Coche: ' + servicioCoche.coche.matricula + ' ' + servicioCoche.servicio.nombre
    })

def eliminar_coche(request, coche_id):
    coche = get_object_or_404(Coche, id=coche_id)
    if request.method == 'POST':
        coche.delete()
        return redirect('lista_coches')
    
    return render(request, 'app_gestion_coches/confirmar_eliminacion.html', {'objeto': coche, 'modelo': 'coche', 'url': 'lista_coches'})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')
    
    return render(request, 'app_gestion_coches/confirmar_eliminacion.html', {'objeto': cliente, 'modelo': 'cliente', 'url': 'lista_clientes'})

def eliminar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    if request.method == 'POST':
        servicio.delete()
        return redirect('lista_servicios')
    
    return render(request, 'app_gestion_coches/confirmar_eliminacion.html', {'objeto': servicio, 'modelo': 'servicio', 'url': 'lista_servicios'})

def eliminar_coche_servicio(request, coche_servicio_id):
    coche_servicio = get_object_or_404(CocheServicio, id=coche_servicio_id)
    if request.method == 'POST':
        coche_servicio.delete()
        return redirect('lista_coches_servicios')
    
    return render(request, 'app_gestion_coches/confirmar_eliminacion.html', {'objeto': coche_servicio, 'modelo': 'servicio de coche', 'url': 'lista_coches_servicios'})
