from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from chucho import settings

from chucho import views

from .views import handler404, handler500, modificar_gasto, modificar_cita, modificar_examen, modificar_tratamiento, modificar_terapia, modificar_cirugia
from .views import eliminar_gasto, eliminar_cita, eliminar_examen, eliminar_tratamiento, eliminar_terapia, eliminar_cirugia

urlpatterns = [
    
## app imports

    path('', include('core.urls')),

### Admin ###
    path('', views.index, name='index'),
    path('admin/', admin.site.urls, name='admin:index'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),

### Lamigo ###
    path('registro/', views.registro, name='registro'),
    path('login2/', views.logeo, name='login2'),
    path('seccion_mascota/', views.seccion_mascota, name='seccion_mascota'),
    path('logout', views.logut_staff, name='logut'),

    # Mascota
    path('mascota/', views.mascota_view, name='mascota'),
    path('gastos/', views.gastos_view, name='gastos'),
    path('citas/', views.citas_view, name='citas'),
    path('examenes/', views.examenes_view, name='examenes'),
    path('tratamientos/', views.tratamientos_view, name='tratamientos'),
    path('terapias/', views.terapias_view, name='terapias'),
    path('cirugias/', views.cirugias_view, name='cirugias'),
    
    #Blog
    path('blog', views.blog, name='blog'),
    path('blog/sobre-nosotros', views.nosotros, name='nosotros'),
    path('blog/actualizaciones', views.actualizaciones, name='actualizaciones'),
    path('blog/arreglos', views.arreglos, name='arreglos'),
    path('blog/avisos', views.avisos, name='avisos'),
    path('blog/politicas', views.politicas, name='politicas'),
    path('blog/preguntas', views.preguntas, name='preguntas'),
    path('blog/servicios', views.servicios, name='servicios'),
    
    #Soportes y contacto
    path('contacto/', views.contacto, name='contacto'),
    path('soporte-tecnico/', views.soporte_tecnico, name='soporte'),
    path('informes-errores/', views.informes_errores, name='informes'),
    
    #Historial CRUD
    path('historial/', views.historial, name='historial'),
    ## CRUD EDIT ##
    # modificacion
    path('modificar_gasto/<int:id>/', modificar_gasto, name='modificar_gasto'),
    path('modificar_cita/<int:id>/', modificar_cita, name='modificar_cita'),
    path('modificar_examen/<int:id>/', modificar_examen, name='modificar_examen'),
    path('modificar_tratamiento/<int:id>/', modificar_tratamiento, name='modificar_tratamiento'),
    path('modificar_terapia/<int:id>/', modificar_terapia, name='modificar_terapia'),
    path('modificar_cirugia/<int:id>/', modificar_cirugia, name='modificar_cirugia'),
    
    #eliminacion
    path('eliminar_gasto/<int:id>/', eliminar_gasto, name='eliminar_gasto'),
    path('eliminar_cita/<int:id>/', eliminar_cita, name='eliminar_cita'),
    path('eliminar_examen/<int:id>/', eliminar_examen, name='eliminar_examen'),
    path('eliminar_tratamiento/<int:id>/', eliminar_tratamiento, name='eliminar_tratamiento'),
    path('eliminar_terapia/<int:id>/', eliminar_terapia, name='eliminar_terapia'),
    path('eliminar_cirugia/<int:id>/', eliminar_cirugia, name='eliminar_cirugia'),
    
    


    
    
    
]

