from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.utils.http import http_date
from .models import Slider, Articulo

# Create your views here.

class Inicio(View):
    def get(self, request):
        qs = Articulo.objects.reverse()[:5]
        context = {
            "slider" : Slider.objects.all(),
            "nuevos" : qs
        }
        return render (self.request, "index.html", context)


class ArticuloDetailView(DetailView):
    model = Articulo
    context_object_name = 'articulo'
    template_name = "productodetail.html"
