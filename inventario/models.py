from django.db import models
import uuid
# Create your models here.

    
class Ingrediente(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

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
    
    def __str__(self):
        return self.nombre
