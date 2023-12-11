from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from chucho import settings

from chucho import views

urlpatterns = [

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
    # gastos
    path('gestionar-g/', views.gestionar_gastos, name='gestionar-g'),
    
    ##Reports
    path('reports/', include('reports.urls')),
    
    
]
