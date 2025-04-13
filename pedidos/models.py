from django.db import models
from inventario.models import Producto
#from users.models import User
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Pedido(models.Model):
    
    id = models.UUIDField(
    primary_key=True,
    default=uuid.uuid4,
    editable=False
    )
    cliente = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='pedidos'
    )
    fecha = models.DateField(auto_now_add=True)
    direccion = models.TextField(max_length=200, default="RETIRO LOCAL")
    delivery = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,  
        null=True, 
        blank=True, 
        related_name='pedidos_asignados'
    )

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente.username}"
    
    @property
    def total(self):
        return sum(
            detalle.producto.precio * detalle.cantidad
            for detalle in self.detalle_pedido.all()
        )

    def __str__(self):
        return f"Pedido {self.id} de {self.usuario.username} - Total: {self.total}"
    
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalle_pedido')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
