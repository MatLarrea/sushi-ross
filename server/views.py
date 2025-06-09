from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import get_resolver
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from users.models import User, Cliente
from .serializers import ClienterSerializer, UserSerializer, productoSerializers, IngredienteSerializer, PedidoSerializer, inventarioSerializers, InsumoSerializer, UserSerializer
from inventario.models import Producto, Ingrediente, Inventario, Insumo
from pedidos.models import DetallePedido, Pedido
from rest_framework.authentication import TokenAuthentication 
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PedidoFilter
from django.db.models import Sum, Count

def api_overview(request):
    resolver = get_resolver()
    urls = []

    for pattern in resolver.url_patterns:
        try:
            url_path = str(pattern.pattern)
            urls.append(url_path)
        except AttributeError:
            pass

    return JsonResponse({"endpoints": urls})

#Usuarios

@api_view(['GET'])
def listar_cajeros_delivery(request):
    users = User.objects.filter(role__in=['CAJERO', 'DELIVERY'])
    serializer = UserSerializer(users, many=True)
    
    # Formatear los datos correctamente
    formatted_data = [
        {"id": user["uuid"], "name": user["name"], "lastname": user["lastname"], "role": user["role"] }
        for user in serializer.data
    ]

    return Response(formatted_data)

@api_view(['POST'])
def login(request):
    
    user = get_object_or_404(User, email=request.data['email'])
    
    if not user.check_password(request.data['password']):
        return Response({'error': 'Contraseña invalida'}, status=status.HTTP_400_BAD_REQUEST)
      
    token, created = Token.objects.get_or_create(user=user)  
    serializer = UserSerializer(instance=user)
    
    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data = request.data)
    
    try:
        if serializer.is_valid():
            user = serializer.save()
            user = User.objects.get(email=serializer.data['email'])
            user.is_active = True
            user.set_password(serializer.data['password'])
            if str(serializer.data['role']).lower() == "administrador":
                user.is_staff = True
            else:
                user.is_staff = False
            user.save()
            
            # Verificar que el usuario existe antes de generar el token
            user = User.objects.get(email=user.email)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'user': serializer.data, 'token': token.key}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    return Response({"mensaje": "autenticado", "user": request.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getUser(request, uuid):
    user = get_object_or_404(User, uuid=uuid)
    serializer =  UserSerializer(user)
    return Response({"id":serializer.data['uuid'],"nombre":serializer.data['name'], "apellido":serializer.data['name']})

@api_view(['GET'])
def getDelivery(request):
    user = User.objects.filter(role="DELIVERY")
    serializer = UserSerializer(user, many=True)
    
    data = serializer.data
    for user in data:
        user.pop("password", None)
    return Response(data, status=status.HTTP_200_OK)

# INVENTARIO
@api_view(['POST'])
def addIngrediente(request):
    serializer = IngredienteSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': f'ingrediente {serializer.data['nombre']} añadido correctamente.',
                         'Ingrediente': serializer.data},
                        status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def addProducto(request):
    serializer = productoSerializers(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': f'producto {serializer.data['nombre']} añadido correctamente.',
                         'producto': serializer.data},
                        status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getIngredientes(request):
    ingredientes = Ingrediente.objects.all() #obtener productos
    serializer = IngredienteSerializer(ingredientes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getProductos(request):
    productos = Producto.objects.filter(creado_por="SISTEMA") #obtener productos
    serializer = productoSerializers(productos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getProducto(request, id):
    # Buscar el producto por el campo nombre
    producto = get_object_or_404(Producto, id=id)
    serializer = productoSerializers(producto)
    return Response(serializer.data)


@api_view(['PATCH'])
def updateProducto(request, id):
    producto = get_object_or_404(Producto, id=id)
    serializer = productoSerializers(producto, data=request.data, partial=True)  # partial=True permite actualización parcial

    if serializer.is_valid():
        serializer.save()  # Guarda los cambios
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['PATCH'])
def updateIngrediente(request, nombre):
    ingrediente = get_object_or_404(Ingrediente, nombre=nombre)
    serializer = IngredienteSerializer(ingrediente, data=request.data, partial=True)  # partial=True permite actualización parcial

    if serializer.is_valid():
        serializer.save()  # Guarda los cambios
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def deleteProducto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if not producto.delete():
        return  Response({"mensaje": f"Error al eliminar {producto.nombre}"})
    
    return  Response({"mensaje": f"Producto eliminado correctamente: {producto.nombre}"})

@api_view(['DELETE'])
def deleteIngrediente(request, nombre):
    ingrediente = get_object_or_404(Ingrediente, nombre=nombre)
    if not ingrediente.delete():
        return  Response({"mensaje": f"Error al eliminar {nombre}"})
    
    return  Response({"mensaje": f"Ingrediente eliminado correctamente: {nombre}"})

#Reportes de ventas
class ReporteVentasViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pedido.objects.filter(estado="ENTREGADO")  # Solo pedidos entregados
    serializer_class = PedidoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PedidoFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())  # Filtramos pedidos según fecha

        # Filtrar los detalles de los pedidos entregados
        detalles_filtrados = DetallePedido.objects.filter(pedido__in=queryset)
            
        total_ventas = sum(float(pedido.total) for pedido in queryset)

        productos_vendidos = detalles_filtrados.values('producto__nombre').annotate(total_vendido=Sum('cantidad'))

        return Response({
            'total_ventas': total_ventas,
            'cantidad_pedidos': queryset.count(),
            'productos_vendidos': list(productos_vendidos),
        })

    
#Pedidos
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PedidoFilter
        
    def perform_create(self, serializer):
        # Guarda el pedido y crea las relaciones inversas
        validated_data = serializer.validated_data
        detalles_data = validated_data.pop('detalle_pedido', [])
        
        # Crear el pedido
        pedido = Pedido.objects.create(**validated_data)
        
        # Crear las instancias de detalle relacionadas
        for detalle_data in detalles_data:
            DetallePedido.objects.create(pedido=pedido, **detalle_data)
        
        serializer.instance = pedido
    
    def perform_update(self, serializer):
        pedido = serializer.instance  # Obtiene la instancia actual
        
        for attr, value in serializer.validated_data.items():
            setattr(pedido, attr, value)  # Actualiza los campos
        pedido.clean()  
        pedido.save()
        serializer.instance = pedido

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienterSerializer
    permission_classes = [permissions.AllowAny]       
    
#Default viewsets
class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = inventarioSerializers
    permission_classes = [permissions.AllowAny]
    
    
class InsumoViewSet(viewsets.ModelViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer
    permission_classes = [permissions.AllowAny]
    
class ProjectDefaultView(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PedidoSerializer 