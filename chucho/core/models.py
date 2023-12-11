from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from .choices import TYPES_DISEASES, TYPES_CITES, TYPES_BILLS, TYPES_SURGERYS, TYPES_EXAMNS

class mascota(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_mascota = models.CharField(max_length=12)
    tipos = models.CharField(max_length=64)
    raza = models.CharField(max_length=32)
    sexo = models.CharField(max_length=10)
    edad = models.CharField(max_length=10)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_mascota

    class Meta:
        ordering = ['id']

class citas(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=12)
    tipos = models.CharField(max_length=64)
    fecha = models.DateField()
    costo = models.FloatField()
    mascota = models.ForeignKey(mascota, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['id']


class examenes(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=12)
    tipos = models.CharField(max_length=64)
    costo = models.FloatField()
    diagnosticos= models.CharField(max_length=512, verbose_name="diagnosticos")
    fecha = models.DateField()
    mascota = models.ForeignKey(mascota, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['id']

class tratamientos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=12)
    fecha = models.DateField()
    costo = models.FloatField()
    mascota = models.ForeignKey(mascota, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['id']

class terapias(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=12)
    fecha = models.DateField()
    costo = models.FloatField()
    mascota = models.ForeignKey(mascota, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['id']
    
class cirugias(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=12)
    tipos = models.CharField(max_length=64)
    fecha = models.DateField()
    costo = models.FloatField()
    mascota = models.ForeignKey(mascota, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['id']
        
class gastos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=12)
    tipos = models.CharField(max_length=64)
    fecha = models.DateField()
    costo = models.FloatField()
    mascota = models.ForeignKey(mascota, on_delete=models.CASCADE)
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['id']



