from django.urls import path 
from .views import (Inicio,
                    ArticuloDetailView,
                    ListaCarritoView,
                    add_to_cart,
                    remove_single_to_cart
                    )

app_name = "core"

urlpatterns = [
    path('', Inicio.as_view(), name="inicio"),
    path('producto/<pk>/', ArticuloDetailView.as_view(), name="producto"),
    path('lista_carrito/', ListaCarritoView.as_view(), name="lista_carrito"),
    path('add_to_cart/<pk>/', add_to_cart, name="add_to_cart"),
    path('remove_single_to_cart/<pk>/', remove_single_to_cart, name="remove_single_to_cart")
]