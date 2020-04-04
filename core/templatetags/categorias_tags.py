from django import template
from core.models import Categorias

register = template.Library()

@register.simple_tag
def mostrar_categorias():
    categorias = Categorias.objects.all()
    return categorias