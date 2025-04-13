from pedidos.models import Pedido
from rest_framework import viewsets, permissions
from server.serializers import PedidoSerializer

class ProjectDefaultView(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PedidoSerializer 