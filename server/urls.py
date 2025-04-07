"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import addProducto, addIngrediente, getProductos, getProducto, getIngredientes, updateIngrediente, updateProducto, deleteProducto, deleteIngrediente, addPedido, deletePedido, getPedidos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('addProduct/', addProducto),
    path('addIngredient/', addIngrediente),
    path('Products/', getProductos),
    path('Ingredients/', getIngredientes),
    path('Products/<str:nombre>/', getProducto, name='getProducto'),
    path('Products/Update/<str:nombre>/', updateProducto, name='updateProducto'),
    path('Ingredients/Update/<str:nombre>/', updateIngrediente, name='updateIngrediente'),
    path('Products/Delete/<str:nombre>/', deleteProducto, name='deleteProducto'),
    path('Ingredients/Delete/<str:nombre>/', deleteIngrediente, name='deleteIngrediente'),
    path('Orders/', getPedidos),
    path('Orders/Generate/', addPedido),
    path('Orders/Delete/<uuid:id>', deletePedido, name='deletePedido'),
]
