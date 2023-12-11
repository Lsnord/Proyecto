from django.urls import path

from reports.views import reportcite

urlpatterns = [

### Reporte de citas ###
    path('cita', reportcite.as_view(), name='cita_report'),
]