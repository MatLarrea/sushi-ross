from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
# Create your models here.

    
class Ingrediente(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    disponible = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(max_length=200)
    ingredientes = models.ManyToManyField(Ingrediente, related_name='productos')
    precio = models.DecimalField(max_digits=10, decimal_places=2) 
    categoria = models.CharField(max_length=20,
                                 choices=[
                                            ('ROLL', 'roll'),
                                            ('BEBESTIBLE', 'bebestible'),
                                            ('CEVICHE', 'ceviche'),
                                            ('HANDROLL', 'handroll'),
                                            ('SUSHIBURGER', 'sushiburger'),
                                            ('EXTRA', 'extra'),
                                            ('GOHAN', 'gohan'),
                                        ])
    disponible = models.BooleanField(default=True)
    creado_por = models.CharField(max_length=50, blank=False, null=False, choices=[
        ("CLIENTE","cliente"),
        ("SISTEMA","sistema")
    ])
    def __str__(self):
        return self.nombre


class Insumo(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    nombre = models.CharField(max_length=20, blank=False, unique=True)
    cantidad = models.IntegerField(validators=[MinValueValidator(0)])
    disponible = models.BooleanField(default=True)
    unidad_medida = models.CharField(max_length=10, choices=[('KG', 'kg'),('LT', 'lt'), ('UNIDAD', 'unidad')])
    
    def __str__(self):
        return f'{self.nombre}: {self.cantidad}{self.unidad_medida}'


class Inventario(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    insumos = models.ManyToManyField(Insumo, related_name='insumos', blank=True)
    
    def save(self, *args, **kwargs):
        if not self.pk and Inventario.objects.exists():
            raise ValueError("Solo puede existir una instancia del modelo Inventario.")
        super(Inventario, self).save(*args, **kwargs)

    def __str__(self):
        return self.id
    
