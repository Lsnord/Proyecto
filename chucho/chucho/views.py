# DJANGO
from email import message
from sre_constants import SUCCESS
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect


#Historial
# Nada por ahora #
##

#forms

from .forms import CitasForm
from .forms import GastoForm, CitasForm, ExamenesForm, TratamientosForm, TerapiasForm, CirugiasForm

#Ping de redireccion
import time

#JSON RESPONSE
from django.http import JsonResponse

# RESTRICCION DE FORMULARIOS
from django.contrib.auth.decorators import user_passes_test

# LAMIGO
from chucho.forms import UserRegisterForm
from chucho.forms import LoginForm
from chucho.forms import formcontact
from chucho.forms import formsoporte
from chucho.forms import forminformes

# Models mios
from core.models import gastos
from core.models import cirugias
from core.models import terapias
from core.models import mascota
from core.models import citas
from core.models import examenes
from core.models import tratamientos

# CHOICES
from core.choices import GENDER_CHOICES
from core.choices import GENDER_PET_CHOICES
from core.choices import PET_TYPES
from core.choices import PET_AGES
from core.choices import TYPES_DISEASES
from core.choices import TYPES_CITES
from core.choices import TYPES_BILLS
from core.choices import TYPES_SURGERYS
from core.choices import TYPES_EXAMNS

# LOGIN SUPERUSER
def login_view(request):
    if request.user.is_authenticated and not request.user.is_staff:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Bienvenido, {}!'.format(user.username))
                return redirect('index')
            else:
                messages.error(request, 'Usuario o contrasena incorrectos')
    return render(request, 'login.html', {})

# LOGOUT SUPERUSER

def logout_view(request):
    if request.user.is_authenticated and not request.user.is_staff:
        logout(request)
        messages.success(request, 'Sesion finalizada')
    return redirect('index')

# LAMIGO #################################################################################################

# PAGINA PRINCIPAL  #
def index(request):
    return render(request, 'index.html', {
        #context
    })


###################### Vistas de Usuario autenticado no staff ############################

# CREACION DE CUENTA USUARIO COMUN

def registro(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}, a Lamigo')

            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, "registro.html", {'form': form})
    
# INICIO DE SESION USUARIO COMUN

def logeo(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Usuario {user.username} logeado')
                return redirect('index')
            else:
                messages.error(request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.')
                # Añadir el mensaje de error al formulario
                form.add_error(None, 'Credenciales inválidas. Contraseña o usuario incorrectos.')
    else:
        form = LoginForm()
    return render(request, "login.html",{'form':form})


## CERRADO DE SESION USUARIO COMUN

def logut_staff(request):
    if not request.user.is_staff:
        logout(request)
    return redirect('index')

#################### Vistas de la mascota ########################################

## Historial

@login_required
def historial(request):
    
    user_bills = gastos.objects.filter(mascota__user=request.user)
    user_cites = citas.objects.filter(mascota__user=request.user)
    user_examns = examenes.objects.filter(mascota__user=request.user)
    user_treatments = tratamientos.objects.filter(mascota__user=request.user)
    user_terapies = terapias.objects.filter(mascota__user=request.user)
    user_surgerys = cirugias.objects.filter(mascota__user=request.user)
    
    return render(request, 'historial.html', {
        'user_bills': user_bills,
        'user_cites': user_cites,
        'user_examns': user_examns,
        'user_treatments': user_treatments,
        'user_terapies': user_terapies,
        'user_surgerys': user_surgerys,
    })



## PAGINA PRINCIPAL DE MASCOTA

def seccion_mascota(request):
    return render(request, 'seccion_mascota.html', {
        #context
    })


## FORMULARIO DE MASCOTA
@login_required
def mascota_view(request):
    error_message = None

    if request.method == 'POST':
        nombre_mascota = request.POST['nombre_mascota']
        edad = request.POST['edad']
        tipos = request.POST['tipos']
        sexo = request.POST['sexo']
        raza = request.POST['raza']
        
        existing_pet = mascota.objects.filter(nombre_mascota=nombre_mascota, edad=edad, tipos=tipos, sexo=sexo, raza=raza, user=request.user).first()
        if existing_pet:
            error_message = 'Ya existe una mascota con estos datos.'
        else:
            new_pet = mascota(nombre_mascota=nombre_mascota, edad=edad, tipos=tipos, sexo=sexo, raza=raza, user=request.user)
            new_pet.save()

            messages.success(request, 'Mascota registrada correctamente.')
            
            return redirect('seccion_mascota')
    
    return render(request, 'mascota.html', {'PET_AGES': PET_AGES, 'PET_TYPES': PET_TYPES, 'GENDER_PET_CHOICES': GENDER_PET_CHOICES, 'error_message': error_message})

# FORMULARIO DE GASTOS DE MASCOTA

@login_required
def gastos_view(request):
    error_message = None
    

    if request.method == 'POST':
        nombre =request.POST['nombre']
        tipos = request.POST['tipos']
        fecha = request.POST['fecha']
        costo = request.POST['costo']
        mascota_id = request.POST['mascota']

        existing_pet = mascota.objects.filter(id=mascota_id, user=request.user).first()

        if not existing_pet:
            error_message = 'Seleccione una mascota válida.'
        else:
            existing_bill = gastos.objects.filter(nombre=nombre, tipos=tipos, fecha=fecha, costo=costo, mascota=existing_pet)
            if existing_bill:
                error_message = 'Ya existe una cita con estos datos para esta mascota.'
            else:
                new_bill = gastos(nombre=nombre, tipos=tipos, fecha=fecha, costo=costo, mascota=existing_pet)
                new_bill.save()
                
                messages.success(request, 'Gasto registrada exitosamente.')
                
                return redirect('seccion_mascota')
            
    user_pets = mascota.objects.filter(user=request.user)
    return render(request, 'gastos.html', {'TYPES_BILLS': TYPES_BILLS, 'user_pets': user_pets, 'error_message': error_message})
#

## CRUD_gasto ##

@login_required
def modificar_gasto(request, id):
    gasto = get_object_or_404(gastos, id=id)
    
    if request.method == 'POST':
        formulario = GastoForm(request.POST, instance=gasto)
        if formulario.is_valid():
            formulario.save()
            return redirect('historial')
    else:
        formulario = GastoForm(instance=gasto)

    return render(request, 'crud/modificar_gasto.html', {'form': formulario})

@login_required
def eliminar_gasto(request, id):
    gasto = get_object_or_404(gastos, id=id)
    gasto.delete()
    return redirect(to='historial')

# FORMULARIO DE CITAS DE MASCOTA
@login_required
def citas_view(request):
    error_message = None

    if request.method == 'POST':
        nombre = request.POST['nombre']
        tipos = request.POST['tipos']
        fecha = request.POST['fecha']
        costo = request.POST['costo']
        mascota_id = request.POST['mascota']

        existing_pet = mascota.objects.filter(id=mascota_id, user=request.user).first()

        if not existing_pet:
            error_message = 'Seleccione una mascota válida.'
        else:
            existing_cite = citas.objects.filter(nombre=nombre, tipos=tipos, fecha=fecha, costo=costo, mascota=existing_pet)
            if existing_cite:
                error_message = 'Ya existe una cita con estos datos para esta mascota.'
            else:

                new_cite = citas(nombre=nombre, tipos=tipos, fecha=fecha, costo=costo, mascota=existing_pet)
                new_cite.save()

                messages.success(request, 'Cita registrada exitosamente.')

                return redirect('seccion_mascota')

    user_pets = mascota.objects.filter(user=request.user)
    return render(request, 'citas.html', {'TYPES_CITES': TYPES_CITES, 'user_pets': user_pets, 'error_message': error_message})

## CRUD_cita ##

@login_required
def modificar_cita(request, id):
    cita = get_object_or_404(citas, id=id)
    
    if request.method == 'POST':
        formulario = CitasForm(request.POST, instance=cita)
        if formulario.is_valid():
            formulario.save()
            return redirect('historial')
    else:
        formulario = CitasForm(instance=cita)

    return render(request, 'crud/modificar_cita.html', {'form': formulario})

@login_required
def eliminar_cita(request, id):
    cita = get_object_or_404(citas, id=id)
    cita.delete()
    return redirect(to='historial')

# FORMULARIO DE EXAMENES DE MASCOTA
@login_required
def examenes_view(request):
    error_message = None
    user_pets = mascota.objects.filter(user=request.user)

    if request.method == 'POST':
        nombre =request.POST['nombre']
        tipos = request.POST['tipos']
        fecha = request.POST['fecha']
        costo = request.POST['costo']
        mascota_id = request.POST['mascota']

        existing_pet = mascota.objects.filter(id=mascota_id, user=request.user).first()

        if not existing_pet:
            error_message = 'Seleccione una mascota válida.'
        else:
            existing_examn = examenes.objects.filter(nombre=nombre, tipos=tipos, fecha=fecha, costo=costo, mascota=existing_pet)
            if existing_examn:
                error_message = 'Ya existe un examen con estos datos para esta mascota.'
            else:
                
                new_examn = examenes(nombre=nombre, tipos=tipos, fecha=fecha, costo=costo, mascota=existing_pet)
                new_examn.save()
                
                messages.success(request, 'Examen registrado exitosamente.')
                return redirect('seccion_mascota')

    return render(request, 'examenes.html', {'TYPES_EXAMNS': TYPES_EXAMNS, 'user_pets': user_pets, 'error_message': error_message})

## CRUD_examenes ##

@login_required
def modificar_examen(request, id):
    examen = get_object_or_404(examenes, id=id)
    
    if request.method == 'POST':
        formulario = ExamenesForm(request.POST, instance=examen)
        if formulario.is_valid():
            formulario.save()
            return redirect('historial')
    else:
        formulario = ExamenesForm(instance=examen)

    return render(request, 'crud/modificar_examen.html', {'form': formulario})

@login_required
def eliminar_examen(request, id):
    examen = get_object_or_404(examenes, id=id)
    examen.delete()
    return redirect(to='historial')

# FORMULARIO DE TRATAMIENTOS DE MASCOTA

def tratamientos_view(request):
    error_message = None
    user_pets = mascota.objects.filter(user=request.user)

    if request.method == 'POST':
        nombre =request.POST['nombre']
        fecha = request.POST['fecha']
        costo = request.POST['costo']
        mascota_id = request.POST['mascota']

        existing_pet = mascota.objects.filter(id=mascota_id, user=request.user).first()

        if not existing_pet:
            error_message = 'Seleccione una mascota válida.'
        else:
            existing_treatment = tratamientos.objects.filter(nombre=nombre, fecha=fecha, costo=costo)
            if existing_treatment:
                error_message = 'Ya existe un tratamiento con estos datos para esta mascota.'
            else:
                
                new_treatment = tratamientos(nombre=nombre, fecha=fecha, costo=costo, mascota=existing_pet)
                new_treatment.save()

                messages.success(request, 'Tratamiento registrado exitosamente.')

                return redirect('seccion_mascota')

    return render(request, 'tratamientos.html', {'user_pets': user_pets, 'error_message': error_message})

## CRUD_tratamientos ##

@login_required
def modificar_tratamiento(request, id):
    tratamiento = get_object_or_404(tratamientos, id=id)
    
    if request.method == 'POST':
        formulario = TratamientosForm(request.POST, instance=tratamiento)
        if formulario.is_valid():
            formulario.save()
            return redirect('historial')
    else:
        formulario = TratamientosForm(instance=tratamiento)

    return render(request, 'crud/modificar_tratamiento.html', {'form': formulario})

@login_required
def eliminar_tratamiento(request, id):
    tratamiento = get_object_or_404(tratamientos, id=id)
    tratamiento.delete()
    return redirect(to='historial')

# FORMULARIO DE TERAPIAS DE MASCOTA

def terapias_view(request):
    error_message = None
    user_pets = mascota.objects.filter(user=request.user)

    if request.method == 'POST':
        nombre =request.POST['nombre']
        fecha = request.POST['fecha']
        costo = request.POST['costo']
        mascota_id = request.POST['mascota']

        existing_pet = mascota.objects.filter(id=mascota_id, user=request.user).first()

        if not existing_pet:
            error_message = 'Seleccione una mascota válida.'
        else:
            existing_terapie = terapias.objects.filter(nombre=nombre, fecha=fecha, costo=costo)

            if existing_terapie:
                error_message = 'Ya existe una terapia con estos datos para esta mascota.'
            else:
                
                new_terapie = terapias(nombre=nombre, fecha=fecha, costo=costo, mascota=existing_pet)
                new_terapie.save()

                messages.success(request, 'Terapia registrada exitosamente.')

                return redirect('seccion_mascota')

    if error_message:
        messages.error(request, error_message)

    return render(request, 'terapias.html', {'user_pets': user_pets})

## CRUD_terapias ##

@login_required
def modificar_terapia(request, id):
    terapia = get_object_or_404(terapias, id=id)
    
    if request.method == 'POST':
        formulario = TerapiasForm(request.POST, instance=terapia)
        if formulario.is_valid():
            formulario.save()
            return redirect('historial')
    else:
        formulario = TerapiasForm(instance=terapia)

    return render(request, 'crud/modificar_terapia.html', {'form': formulario})

@login_required
def eliminar_terapia(request, id):
    terapia = get_object_or_404(terapias, id=id)
    terapia.delete()
    return redirect(to='historial')


# FORMULARIO DE CIRUGIAS DE MASCOTA

def cirugias_view(request):
    error_message = None
    user_pets = mascota.objects.filter(user=request.user)

    if request.method == 'POST':
        nombre =request.POST['nombre']
        tipos = request.POST['tipos']
        fecha = request.POST['fecha']
        costo = request.POST['costo']
        mascota_id = request.POST['mascota']

        existing_pet = mascota.objects.filter(id=mascota_id, user=request.user).first()

        if not existing_pet:
            error_message = 'Seleccione una mascota válida.'
        else:
            existing_surgery = cirugias.objects.filter(nombre=nombre, tipos=tipos, fecha=fecha, costo=costo, mascota=existing_pet)
            if existing_surgery:
                error_message = 'Ya existe una cirugia con estos datos para esta mascota.'
            else:
                
                new_surgery = cirugias(nombre=nombre, tipos=tipos, fecha=fecha, costo=costo, mascota=existing_pet)
                new_surgery.save()
                
                messages.success(request, 'Cirugia registrada exitosamente.')
                return redirect('seccion_mascota')

    return render(request, 'cirugias.html', {'TYPES_SURGERYS': TYPES_SURGERYS, 'user_pets': user_pets, 'error_message': error_message})

## CRUD_terapias ##

@login_required
def modificar_cirugia(request, id):
    cirugia = get_object_or_404(cirugias, id=id)
    
    if request.method == 'POST':
        formulario = CirugiasForm(request.POST, instance=cirugia)
        if formulario.is_valid():
            formulario.save()
            return redirect('historial')
    else:
        formulario = CirugiasForm(instance=cirugia)

    return render(request, 'crud/modificar_cirugia.html', {'form': formulario})

@login_required
def eliminar_cirugia(request, id):
    cirugia = get_object_or_404(cirugias, id=id)
    cirugia.delete()
    return redirect(to='historial')




###################################### Sobre Nosotros ##########################################################

# Blog
def blog(request):
    return render(request, 'blog.html', {
        #context
    })
    
def nosotros(request):
    return render(request, 'blog-nosotros.html', {
        #context
    })

def actualizaciones(request):
    return render(request, 'blog-actualizaciones.html', {
        #context
    })
    
def arreglos(request):
    return render(request, 'blog-arreglos.html', {
        #context
    })
    
def avisos(request):
    return render(request, 'blog-avisos.html', {
        #context
    })
    
def politicas(request):
    return render(request, 'blog-politicas.html', {
        #context
    })
    
def preguntas(request):
    return render(request, 'blog-preguntas.html', {
        #context
    })
    
def servicios(request):
    return render(request, 'blog-servicios.html', {
        #context
    })
    
# Contacto #
def contacto(request):

    if request.method=="POST":

        form=formcontact(request.POST)

        if form.is_valid():

            infForm=form.cleaned_data

            send_mail(infForm['asunto'],['mensaje'],
            infForm.get('email', ''),['blion0010@gmail.com'],)

            return render(request, "gracias.html")
        
    else:

        form=formcontact()

    return render(request,"contacto.html",{"form":form})

#Soporte de tecnico
def soporte_tecnico(request):

    if request.method=="POST":

        form=formsoporte(request.POST)

        if form.is_valid():

            inf1Form=form.cleaned_data

            send_mail(inf1Form['asunto'],['mensaje'],
            inf1Form.get('email', ''),['blion0010@gmail.com'],)

            return render(request, "gracias.html")
        
    else:

        form=formsoporte()

    return render(request,"soporte-tecnico.html",{"form":form})

#Informes de errores

def informes_errores(request):

    if request.method=="POST":

        form=forminformes(request.POST)

        if form.is_valid():

            inf2Form=form.cleaned_data

            send_mail(inf2Form['asunto'],['mensaje'],
            inf2Form.get('email', ''),['blion0010@gmail.com'],)

            return render(request, "gracias.html")
        
    else:

        form=forminformes()

    return render(request,"informes-errores.html",{"form":form})


#errores

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)










