from django import template
from core.models import Categorias

register = template.Library()

@register.filter
def mostrar_categorias():
    return Categorias.objects.all()