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
from django.urls import path, include
from .views import addProducto, addIngrediente, api_overview, getProductos, getProducto, getIngredientes, login, profile, updateIngrediente, updateProducto, deleteProducto, deleteIngrediente, ProjectDefaultView, register
from .routers import ruoter

urlpatterns = [
    path('Sushiross/', ProjectDefaultView.as_view({'get': 'list'})),
    path('admin', admin.site.urls),
    path('addProduct/', addProducto),
    path('addIngredient/', addIngrediente),
    path('Products/', getProductos),
    path('Ingredients/', getIngredientes),
    path('Products/<str:id>/', getProducto, name='getProducto'),
    path('Products/Update/<str:id>/', updateProducto, name='updateProducto'),
    path('Ingredients/Update/<str:nombre>/', updateIngrediente, name='updateIngrediente'),
    path('Products/Delete/<str:id>/', deleteProducto, name='deleteProducto'),
    path('Ingredients/Delete/<str:nombre>/', deleteIngrediente, name='deleteIngrediente'),
    path('users/register/', register, name='register'),
    path('users/login/', login, name='login'),
    path('users/profile/', profile, name='profile'),
    path('', include(ruoter.urls)),
    path('Endpoints/', api_overview, name='api-overview'),
]


    #  addPedido, deletePedido, getPedidos,
    # path('Orders/', getPedidos),
    # path('Orders/Generate/', addPedido),
    # path('Orders/Delete/<uuid:id>', deletePedido, name='deletePedido'),