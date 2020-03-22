from django.urls import path 
from .views import (Inicio,
                    ArticuloDetailView
                    )

app_name = "core"

urlpatterns = [
    path('', Inicio.as_view(), name="inicio"),
    path('producto/<pk>/', ArticuloDetailView.as_view(), name="producto")
]