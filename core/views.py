from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.utils.http import http_date
from django.core.exceptions import ObjectDoesNotExist
from .models import Slider, Articulo, Categorias

# Create your views here.

class Inicio(View):
    def get(self, request):
        qs = Articulo.objects.reverse()[:5]
        get_categorias = Categorias.objects.all()
        context = {
            "slider" : Slider.objects.all(),
            "nuevos" : qs,
            "categoria" : get_categorias
        }
        return render (self.request, "index.html", context)


class ArticuloDetailView(DetailView):
    model = Articulo
    context_object_name = 'articulo'
    template_name = "productodetail.html"

    def get_object(self,):
        try:
            articulo = Articulo.objects.get(pk=self.kwargs['pk'])
            mas_producto =Articulo.objects.filter(categoria=articulo.categoria)
            context = {
                'articulo' : articulo,
                'mas_producto' : mas_producto
            }

        except ObjectDoesNotExist:
            return 0

        return context

        
