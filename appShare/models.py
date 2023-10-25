# from django.core.exceptions import ValidationError este es un modulo que nos permite validar yo use uno personalizado para aprender
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
class MyCustomException(Exception):
    def __init__(self,errors):
        self.errors = errors
    def __str__(self):
        return repr(self.errors)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Implementa la lógica para crear un usuario
        # ...
        pass
    def create_superuser(self, email, password=None, **extra_fields):
        # Implementa la lógica para crear un superusuario
        # ...
        pass

    def get_by_natural_key(self, username):
        return self.get(email=username)

# Create your models here.
# Cuando creas un modelo personalizado como lop hago yo necesitas heredar de AbstractBaseUser
# y tambien debes colocar una propiedad USERNAME_FIELD que vas a usar
# todo esto para poder usar el metodo login de python para guardar los datos en una cookie
class Users(AbstractBaseUser):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=80,unique=True)
    password = models.CharField(max_length=300)
    telefono = models.CharField(max_length=10)
    admin = models.BooleanField(default=False)
    confirmado = models.BooleanField(default=False)
    token = models.TextField(default='')
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def validatorCamp(self):
        errors = []
        print("probandoo", self.password)
        if not self.nombre:
              errors.append("El nombre es oblogatorio.")
        if not self.apellido:
            errors.append("El apellido es obligatorio")
        if not self.email:
            errors.append("El email es obligatorio")
        if not self.password:
            errors.append("El password es obligatorio")
        if not self.telefono:
            errors.append("El telefono es obligatorio")
        elif not self.telefono.isdigit():
            errors.append("El telefono tiene que ser  numeros no un texto ejemplo 3876223417")
        elif  len(self.telefono) < 10:
            errors.append("El numero de telefono tiene que contener al menos 10 digitos")
        if '<' in self.nombre or '>' in self.nombre or '.' in self.nombre:
            errors.append("El nombre no puede contener simbolos")
        if '<' in self.apellido or '>' in self.apellido or '.' in self.apellido:
            errors.append("El apellido no puede contener simbolos")
        if errors:
            raise MyCustomException(errors)
        
    def ValidatorCampLogin(self,error=[]):
        errors = []
        if len(error) > 0 :
            for element in error:
                errors.append(element)
        if not self.email:
             errors.append("El email es obligatorio")
        if not self.password:
            errors.append("El password es obligatorio")
        if errors:
            raise MyCustomException(errors)
    
class Citas(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    usuarioId = models.ForeignKey(Users, on_delete=models.CASCADE)
 

class Servicios(models.Model):
    nombre = models.CharField(max_length=90)
    precio = models.FloatField()
  
class CitasServicios(models.Model):
    citaId = models.ForeignKey(Citas, on_delete=models.CASCADE)
    serviciosId = models.ForeignKey(Servicios, on_delete=models.CASCADE)
