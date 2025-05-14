from datetime import datetime
from django.db import models
from django.forms import ValidationError
from inventario.models import Producto
#from users.models import User
from users.models import User, Cliente
import uuid

# Create your models here.
class Pedido(models.Model):
    
    id = models.UUIDField(
    primary_key=True,
    default=uuid.uuid4,
    editable=False
    )
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos', null=True, blank=True)
    cliente_db = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos', null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    direccion = models.TextField(max_length=200, default="RETIRO LOCAL", blank=True)
    estado = models.CharField(max_length=20,default="PREPARACION",
                                 choices=[
                                            ('PREPARACION', 'preparacion'),
                                            ('REPARTO', 'reparto'),
                                            ('LISTO', 'listo'),
                                            ('ENTREGADO', 'entregado'),
                                            ('CANCELADO', 'cancelado'),
                                        ])
    delivery = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,  
        null=True, 
        blank=True, 
        related_name='pedidos_asignados'
    )
    cajero = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,  
        null=True, 
        blank=True, 
        related_name='pedidos_ingresados'
    )
    observacion = models.TextField(max_length=200, blank=True)
    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente.full_name}"
    
    @property
    def total(self):
        return sum(
            detalle.producto.precio * detalle.cantidad
            for detalle in self.detalle_pedido.all()
        )


    def clean(self):
        # Validación para que solo uno de los dos campos tenga valor
        if self.pk is None and not self.cliente and not self.cliente_db:
            raise ValidationError("Debe haber un valor en 'cliente' o en 'cliente_db'.")
    
    def update(self, instance, validated_data):
        # Iterar sobre los campos para realizar la actualización parcial
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()  # Guardar la instancia con los cambios
        return instance
         
    def __str__(self):
        return f"Pedido {self.id} de {self.usuario.username} - Total: {self.total}"
    
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalle_pedido')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
