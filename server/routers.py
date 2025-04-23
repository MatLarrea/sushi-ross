from rest_framework import routers
from .views import InventarioViewSet, InsumoViewSet, PedidoViewSet, ClienteViewSet   

ruoter = routers.DefaultRouter()
ruoter.register(r'Inventario', InventarioViewSet)
ruoter.register(r'Insumo', InsumoViewSet)
ruoter.register(r'Pedido', PedidoViewSet)
ruoter.register(r'Cliente', ClienteViewSet)

print(ruoter.urls)