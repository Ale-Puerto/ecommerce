from django.urls import path 
from .views import (Inicio,
                    ArticuloDetailView,
                    add_to_cart
                    )

app_name = "core"

urlpatterns = [
    path('', Inicio.as_view(), name="inicio"),
    path('producto/<pk>/', ArticuloDetailView.as_view(), name="producto"),
    path('add_to_cart/<pk>/', add_to_cart, name="add_to_cart")
]