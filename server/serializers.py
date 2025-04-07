from rest_framework import serializers
from inventario.models import Producto, Ingrediente
from pedidos.models import Pedido, DetallePedido
from django.contrib.auth.models import User

#Inventario
class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ['id','nombre']
        
class productoUpdateSerializers(serializers.ModelSerializer):
    ingredientes = serializers.PrimaryKeyRelatedField(many=True, queryset=Ingrediente.objects.all())
    
    class Meta:
        model = Producto
        fields = ['id','nombre', 'descripcion', 'categoria', 'ingredientes']

class productoAddSerializers(serializers.ModelSerializer):
    ingredientes = serializers.PrimaryKeyRelatedField(many=True, queryset=Ingrediente.objects.all())
    
    class Meta:
        model = Producto
        fields = ['id','nombre', 'descripcion', 'categoria', 'ingredientes', 'precio']
        
    def create(self, validated_data):
        ingredientes = validated_data.pop('ingredientes')
        producto = Producto.objects.create(**validated_data)
        producto.ingredientes.set(ingredientes)
        return producto

    def update(self, instance, validated_data):
        ingredientes = validated_data.pop('ingredientes')
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.save()
        instance.ingredientes.set(ingredientes)
        return instance
        
class productoSerializers(serializers.ModelSerializer):
    ingredientes = ingredientes = IngredienteSerializer(many=True)
    
    class Meta:
        model = Producto
        fields = ['id','nombre', 'descripcion', 'categoria', 'ingredientes']
        

#Pedido
class DetallePedidoSerializer(serializers.ModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())

    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']
        
class PedidoSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    detalle_pedido = DetallePedidoSerializer(many=True)  # Use the related_name here
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'fecha', 'detalle_pedido', 'total']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalle_pedido')
        pedido = Pedido.objects.create(**validated_data)

        # Create or link DetallePedido instances
        for detalle_data in detalles_data:
            DetallePedido.objects.create(pedido=pedido, **detalle_data)

        return pedido

        
