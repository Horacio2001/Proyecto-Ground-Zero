
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models  import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from .serializers import *
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


import urllib.parse
import requests
import json

import os


# Create your views here.


def register(request):

    aux = { 
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save()
            group = Group.objects.get(name='Usuario')
            user.groups.add(group)

            return redirect(to="login")
        else:
            aux["form"]= formulario

    return render(request, 'registration/register.html',aux)

def index(request):
    obras = Obra.objects.all()
    data = {
        'obras': obras
    }
    return render(request, 'core/index.html', data)


def login(request):
    return render(request, 'core/registration/login.html')

@permission_required('core.view_obra')
def gestion(request):
    obras = Obra.objects.all()
    
    data = { 
        'obras': obras
    }
    return render(request, 'core/imagenes/crud/gestion.html',data)

@permission_required('core.add_obra')
def agregar_autor(request):
    
    data = {
        'form':ObraForm()
    }

    if request.method == 'POST':
        formulario = ObraForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Solicitud enviada correctamente" 
        else:
            data["form"]= formulario

    return render(request, 'core/Imagenes/crud/add.html',data)


@permission_required('core.change_obra')
def modificar_obra(request, id_obra):
    obra = get_object_or_404(Obra, id_obra=id_obra)
    
    if request.method == 'POST':
        formulario = ObraForm(request.POST, request.FILES, instance=obra)
        if formulario.is_valid():
            # Si se guarda una nueva imagen, eliminamos la anterior antes 
            if 'imagen' in formulario.changed_data:
                # Eliminar la imagen anterior si existe
                if obra.imagen:
                    obra.imagen.delete()
            formulario.save()
            return redirect('gestion')
    else:
        formulario = ObraForm(instance=obra)
    
    return render(request, 'core/Imagenes/crud/modificar.html', {'form': formulario})

@permission_required('core.delete_obra')
def eliminar_obra(request, id_obra):
    obra = get_object_or_404(Obra, id_obra=id_obra)

    imagen_path = obra.foto.path

    obra.delete()

    if os.path.exists(imagen_path):
        os.remove(imagen_path)
    return redirect(to=gestion)


def contacto(request):
    data = {
        'form': ContactoForm()
    }
    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Mensaje enviado!"
        else:
            data["form"]=formulario
            
    return render(request,'core/contacto.html',data)


def detalle(request, id_obra):
    obra = get_object_or_404(Obra, id_obra=id_obra)
    return render(request, 'core/detalle.html', {'obra': obra})

@login_required
def suscripcion(request):
    return render(request, 'core/suscripcion.html')

def bloqueo_view(request):
    return render(request, 'registration/Bloqueo.html')

def voucher(request):
    return render(request, 'core/voucher.html')

#agregar pagina historial
def historial(request):
    return render(request, 'core/historial.html')

# Nuestras APIS
class TipoEmpleadoViewSet(viewsets.ModelViewSet):
    queryset = TipoEmpleado.objects.all().order_by('id')
    serializer_class = TipoEmpleadoSerializer
    renderer_classes = [JSONRenderer]
class GeneroViewSet(viewsets.ModelViewSet):
    queryset = TipoGenero.objects.all().order_by('id')
    serializer_class = GeneroSerializer
    renderer_classes = [JSONRenderer]
class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all().order_by('id')
    serializer_class = EmpleadoSerializer
    renderer_classes = [JSONRenderer]

def empleadosapi(request):
    response = requests.get('https://api.artic.edu/api/v1/artworks?page=2&limit=100')
    artworks = response.json()
    lista = artworks['data']

    # Crear el paginador
    paginator = Paginator(lista, 3)  # Muestra 10 elementos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'core/Imagenes/crudapi/index.html', context)


def dineroapi(request):
    response = requests.get('https://mindicador.cl/api')
    dinero = response.json()

    if 'version' in dinero:
        del dinero['version']
    if 'autor' in dinero:
        del dinero['autor']
    if 'fecha' in dinero:
        del dinero['fecha']

    aux = {
        'lista' : dinero
    }
    return render(request,'core/Imagenes/crudapi/detalle.html', aux)

#guardar pago
@csrf_exempt
def guardar_pago(request):
    if request.method == 'POST':
        # Obtener los datos del pago del cuerpo de la solicitud POST
        identificador_venta = request.POST.get('identificador_venta')
        nombre_usuario = request.POST.get('nombre_usuario')
        monto = request.POST.get('monto')
        nombre_plan = request.POST.get('nombre_plan')

        # Guardar el pago en la base de datos
        pago = Pago(
            identificador_venta=identificador_venta,
            nombre_usuario=nombre_usuario,
            monto=monto,
            nombre_plan=nombre_plan
        )
        pago.save()

        # Opcional: Puedes devolver una respuesta JSON si lo deseas
        return JsonResponse({'mensaje': 'Pago registrado correctamente.'})
    else:
        # Manejar otros métodos HTTP si es necesario
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
#poner si es que una su
def suscripcion(request):
    # Obtener el pago más reciente del usuario autenticado
    ultimo_pago = Pago.objects.filter(nombre_usuario=request.user.username).order_by('-fecha_pago').first()

    # Inicializar variables de estado de los planes
    plan_basico_adquirido = False
    plan_estandar_adquirido = False
    plan_premium_adquirido = False

    if ultimo_pago:
        if ultimo_pago.nombre_plan == 'Plan Básico':
            plan_basico_adquirido = True
        elif ultimo_pago.nombre_plan == 'Plan Estándar':
            plan_estandar_adquirido = True
        elif ultimo_pago.nombre_plan == 'Plan Premium':
            plan_premium_adquirido = True

    context = {
        'plan_basico_adquirido': plan_basico_adquirido,
        'plan_estandar_adquirido': plan_estandar_adquirido,
        'plan_premium_adquirido': plan_premium_adquirido,
    }

    return render(request, 'core/suscripcion.html', context)

#recuperar datos de pago 
def voucher(request):
    # Filtra los pagos del usuario autenticado
    if request.user.is_authenticated:
        pagos = Pago.objects.filter(nombre_usuario=request.user).order_by('-fecha_pago')
    else:
        pagos = []

    context = {
        'pagos': pagos  # Pasar los pagos del usuario al contexto
    }

    return render(request, 'core/voucher.html', context)

def generar_pdf(request, pago_id):
    # Obtener el objeto de Pago desde la base de datos
    pago = get_object_or_404(Pago, pk=pago_id)

    # Crear la respuesta HTTP para el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="voucher_pago_{pago_id}.pdf"'

    # Configurar el lienzo (canvas) para generar el PDF
    pdf = canvas.Canvas(response, pagesize=letter)

    # Configurar fuentes y estilos
    pdf.setFont("Helvetica-Bold", 16)
    pdf.setFillColorRGB(0.2, 0.4, 0.6)  # Color de relleno azul oscuro

    # Título del voucher
    pdf.drawString(100, 750, 'Voucher de Pago')
    pdf.line(100, 745, 300, 745)  # Línea debajo del título

    # Detalles del pago
    pdf.setFont("Helvetica", 12)
    pdf.setFillColorRGB(0, 0, 0)  # Color de relleno negro
    pdf.drawString(100, 720, f'ID del Pago: {pago.id}')
    pdf.drawString(100, 700, f'Usuario: {pago.nombre_usuario}')
    pdf.drawString(100, 680, f'Monto: ${pago.monto}')
    pdf.drawString(100, 660, f'Fecha de Pago: {pago.fecha_pago.strftime("%d/%m/%Y")}')
    pdf.drawString(100, 640, f'Plan: {pago.nombre_plan}')

    # Mensaje de agradecimiento
    pdf.setFont("Helvetica-Oblique", 12)
    pdf.drawString(100, 600, '¡Gracias por tu compra!')

    # Guardar el PDF
    pdf.showPage()  # Mostrar la página actual
    pdf.save()  # Guardar el documento completo

    return response

    