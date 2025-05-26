from rest_framework import routers
from .views import InventarioViewSet, InsumoViewSet, PedidoViewSet, ClienteViewSet, ReporteVentasViewSet   

ruoter = routers.DefaultRouter()
ruoter.register(r'Inventario', InventarioViewSet)
ruoter.register(r'Insumo', InsumoViewSet)
ruoter.register(r'Pedido', PedidoViewSet, basename='pedidos')
ruoter.register(r'Reporte', ReporteVentasViewSet, basename='reporte-ventas')
ruoter.register(r'Cliente', ClienteViewSet)

print(ruoter.urls)