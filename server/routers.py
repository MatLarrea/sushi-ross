from rest_framework import routers
from .views import InventarioViewSet, InsumoViewSet    

ruoter = routers.DefaultRouter()
ruoter.register(r'Inventario', InventarioViewSet)
ruoter.register(r'Insumo', InsumoViewSet)

print(ruoter.urls)