import django_filters
from pedidos.models import Pedido

class PedidoFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name="fecha", lookup_expr="year")
    month = django_filters.NumberFilter(field_name="fecha", lookup_expr="month")
    day = django_filters.NumberFilter(field_name="fecha", lookup_expr="day")
    estado = django_filters.CharFilter(field_name="estado")  
    
    class Meta:
        model = Pedido
        fields = ['year', 'month', 'day', 'estado']
        
    