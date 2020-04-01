from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from django.utils.http import http_date
from django.core.exceptions import ObjectDoesNotExist
from .models import Slider, Articulo, Categorias, ArticuloPedido, Pedido
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
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

class ListaCarritoView(View):
    def get(self, *args,**kwargs):
        try:
            lista = Pedido.objects.get(user=self.request.user, ordenado=False)
            context = {
                'object' : lista
            }
            return render(self.request, "lista_carrito.html", context)
        except ObjectDoesNotExist:
            pass


@login_required
def remove_single_to_cart(request, pk):
  
    articulo = get_object_or_404(Articulo, pk=pk)
    pedido = Pedido.objects.filter(
            user = request.user,
            
            ordenado = False
    )
        
    if pedido.exists():
            pedido = pedido[0]
            if pedido.articulos_pedidos.filter(articulo__pk=articulo.pk).exists():
                articulo_pedido = ArticuloPedido.objects.filter(
                    user = request.user,
                    articulo = articulo,
                    ordenado = False
                )[0]
                if articulo_pedido.cantidad > 1:
                    articulo_pedido.cantidad -= 1
                    articulo_pedido.save()
                    return redirect("core:lista_carrito")
                else:
                    pedido.articulos_pedidos.remove(articulo_pedido)
                    return redirect("core:lista_carrito")
            else:
                return redirect("core:lista_carrito")
    else:
        return redirect("core:inicio")
  

@login_required
def add_to_cart(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)
    articulo_pedido, create = ArticuloPedido.objects.get_or_create(
        user = request.user,
        articulo = articulo,
        ordenado = False
    )
    orden_qs = Pedido.objects.filter(user=request.user, ordenado=False)
    if orden_qs.exists():
        pedido = orden_qs[0]
        if pedido.articulos_pedidos.filter(articulo__pk=articulo.pk).exists():
            articulo_pedido.cantidad += 1
            articulo_pedido.save()
            #RECORDAR AÑADIR MENSAJE 
            return redirect("core:inicio")
        else:
            pedido.articulos_pedidos.add(articulo_pedido)
            pedido.save()
            #Mensaje
            return redirect("core:inicio")
    else:
        fecha_pedido = timezone.now()
        pedido = Pedido.objects.create(
            user=request.user,
            fecha_pedido=fecha_pedido
        )
        pedido.articulos_pedidos.add(articulo_pedido)
        return redirect("core:inicio")