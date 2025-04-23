from rest_framework import serializers
from inventario.models import Producto, Ingrediente, Inventario, Insumo
from pedidos.models import Pedido, DetallePedido
from users.models import User, Cliente

#Inventario
class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ['id','nombre', 'disponible']
        
        
class productoSerializers(serializers.ModelSerializer):
    ingredientes = serializers.PrimaryKeyRelatedField(many=True, queryset=Ingrediente.objects.all())
    creado_por = serializers.CharField(required=True)
    class Meta:
        model = Producto
        fields = '__all__'
        
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
    cliente = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    cliente_db = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all(), required=False, allow_null=True)
    detalle_pedido = DetallePedidoSerializer(many=True) 
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    
    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'cliente_db', 'fecha', 'detalle_pedido', 'total', 'estado']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Cambia el formato de la fecha en la representación
        representation['fecha'] = instance.fecha.strftime("%d-%m-%y %H:%M")
        return representation
    
    def validate(self, data):
            cliente = data.get('cliente', None)
            cliente_db = data.get('cliente_db', None)

            if cliente and cliente_db:
                raise serializers.ValidationError("Un pedido solo puede tener un cliente o un cliente_db, no ambos.")
            elif not cliente and not cliente_db:
                raise serializers.ValidationError("Debe asignarse un cliente o cliente_db al pedido.")

            return data

#Usuario
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uuid","name", "lastname", "cellphone", "email", "password", "role"]
        
class ClienterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'