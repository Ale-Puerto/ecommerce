from django import template
from core.models import Pedido

register = template.Library()

@register.filter
def carrito_conteo(user):
    if user.is_authenticated:
        qs = Pedido.objects.filter(user=user, ordenado=False)
        if qs.exists():
            return qs[0].articulos_pedidos.count()
    return 0
   