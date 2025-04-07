from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import productoSerializers, IngredienteSerializer, productoUpdateSerializers, PedidoSerializer, productoAddSerializers
from inventario.models import Producto, Ingrediente
from pedidos.models import Pedido


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
    serializer = productoAddSerializers(data=request.data)
    
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
    return Response(serializer.data, status=status.HTTP_302_FOUND)


@api_view(['GET'])
def getProductos(request):
    productos = Producto.objects.all() #obtener productos
    serializer = productoSerializers(productos, many=True)
    return Response(serializer.data, status=status.HTTP_302_FOUND)

@api_view(['GET'])
def getProducto(request, nombre):
    # Buscar el producto por el campo nombre
    producto = get_object_or_404(Producto, nombre=nombre)
    serializer = productoSerializers(producto)
    return Response(serializer.data)


@api_view(['PATCH'])
def updateProducto(request, nombre):
    producto = get_object_or_404(Producto, nombre=nombre)
    serializer = productoUpdateSerializers(producto, data=request.data, partial=True)  # partial=True permite actualización parcial

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
def deleteProducto(request, nombre):
    producto = get_object_or_404(Producto, nombre=nombre)
    if not producto.delete():
        return  Response({"mensaje": f"Error al eliminar {nombre}"})
    
    return  Response({"mensaje": f"Producto eliminado correctamente: {nombre}"})

@api_view(['DELETE'])
def deleteIngrediente(request, nombre):
    ingrediente = get_object_or_404(Ingrediente, nombre=nombre)
    if not ingrediente.delete():
        return  Response({"mensaje": f"Error al eliminar {nombre}"})
    
    return  Response({"mensaje": f"Ingrediente eliminado correctamente: {nombre}"})
    
#Pedidos

@api_view(['POST'])
def addPedido(request):
    serializer = PedidoSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje':"Se ha generado el pedido", "pedido":serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getPedidos(request):
    pedidos = Pedido.objects.all()  
    serializer = PedidoSerializer(pedidos, many=True)  
    return Response(serializer.data)

# @api_view(['GET'])
# def getPedidosByDate(request):
#     pedidos = Pedido.objects.all(date)  
#     serializer = PedidoSerializer(pedidos, many=True)  
#     return Response(serializer.data)


@api_view(['DELETE'])
def deletePedido(request, id):
    pedido = get_object_or_404(Producto, id=id)
    if not pedido.delete():
        return  Response({"mensaje": f"Error al eliminar {pedido}"})
    
    return  Response({"mensaje": f"Producto eliminado correctamente: {pedido}"})