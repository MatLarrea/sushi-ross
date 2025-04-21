from rest_framework import serializers
from inventario.models import Producto, Ingrediente, Inventario, Insumo
from pedidos.models import Pedido, DetallePedido
from users.models import User

#Inventario
class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ['id','nombre', 'disponible']
        
class productoUpdateSerializers(serializers.ModelSerializer):
    ingredientes = serializers.PrimaryKeyRelatedField(many=True, queryset=Ingrediente.objects.all())
    
    class Meta:
        model = Producto
        fields = ['id','nombre', 'descripcion', 'categoria', 'ingredientes', 'disponible']

class productoAddSerializers(serializers.ModelSerializer):
    ingredientes = serializers.PrimaryKeyRelatedField(many=True, queryset=Ingrediente.objects.all())
    
    class Meta:
        model = Producto
        fields = ['id','nombre', 'descripcion', 'categoria', 'ingredientes', 'precio', 'disponible']
        
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
    ingredientes = IngredienteSerializer(many=True)
    
    class Meta:
        model = Producto
        fields = ['id','nombre', 'descripcion', 'categoria', 'ingredientes', 'precio', 'disponible']

class InsumoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Insumo
        fields = ['id', 'nombre', 'cantidad', 'unidad_medida','disponible']
        
    def create(self, validated_data):
        # Obtener la instancia única de Inventario
        inventario = Inventario.objects.first()  
        if not inventario:
            raise serializers.ValidationError("No existe un inventario para asociar.")

        # Crear el insumo y asociarlo al inventario
        insumo = Insumo.objects.create(**validated_data)
        inventario.insumos.add(insumo)  # Asociar el insumo al inventario
        return insumo
        
class inventarioSerializers(serializers.ModelSerializer):
    insumos = InsumoSerializer(many=True, required=False)
    
    class Meta:
        model = Inventario
        fields = '__all__'  # Incluye todos los campos del modelo
        read_only_fields = ['id']  # Hace que el campo `id` sea de solo lectura

    def validate(self, data):
        """Evita la creación de más de una instancia de Inventario."""
        if not self.instance and Inventario.objects.exists():
            raise serializers.ValidationError("Solo puede existir una instancia de Inventario.")
        return data
#Pedido
class DetallePedidoSerializer(serializers.ModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())

    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']
        
class PedidoSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    detalle_pedido = DetallePedidoSerializer(many=True) 
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

#Usuario
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","name", "lastname", "cellphone", "email", "password", "role"]