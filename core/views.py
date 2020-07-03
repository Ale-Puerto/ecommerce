from django.shortcuts import render, redirect
from django.views import View
from .forms import DireccionForm, CuponForm
from django.views.generic import DetailView
from django.utils.http import http_date
from django.core.exceptions import ObjectDoesNotExist
from .models import Slider, Articulo, Categorias, ArticuloPedido, Pedido, Direccion
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

def campos_validados(values):
    valido = True
    for campo in values:
        if campo==" ":
            valido = False
    
    return valido


class Inicio(View):
    def get(self, request):
        qs = Articulo.objects.reverse()[:6]
        get_categorias = Categorias.objects.reverse()[:5]
        context = {
            "slider" : Slider.objects.all(),
            "nuevos" : qs,
            "categorias" : get_categorias
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

class PagosView(View):
    def get(self, *args, **kwargs):
        lista = Pedido.objects.get(user=self.request.user, ordenado=False)
        context = {
            'pedido' : lista
        }
        return render (self.request, "pago.html", context)


class VerficarView(View):
    def get(self, *args , **kwargs):
        lista = Pedido.objects.get(user=self.request.user, ordenado=False)
        
        context = {
            'form' : DireccionForm(),
            'cupon' : CuponForm(),
            'pedido' : lista,
            'mostrar_cupon' : True
        }
        direccion_guardada = Direccion.objects.filter(user=self.request.user, default=True)
        if direccion_guardada.exists():
            context.update({'default':direccion_guardada[0]})
        return render(self.request , "revision.html", context)

    def post(self, *args, **kwargs):
        form = DireccionForm(self.request.POST or None)
        try:
            pedido = Pedido.objects.get(user=self.request.user, ordenado=False)
           
            if form.is_valid():
               default = form.cleaned_data.get('default')
               if default:
                   direccion = Direccion.objects.filter(user=self.request.user, default=True)
                   if direccion.exists():
                       direccion_qs = direccion[0]
                       pedido.direccion_envio  = direccion_qs
                       pedido.save()
                       return redirect("core:pago")
                   else:
                        return redirect("core:verificar")
               else:
                    nombre_referencia = form.cleaned_data.get('nombre_referencia')
                    telefono = form.cleaned_data.get('telefono')
                    direccion_especifica = form.cleaned_data.get('direccion_especifica')
                    pais = form.cleaned_data.get('pais')
                    provincia = form.cleaned_data.get('provincia')
                    ciudad = form.cleaned_data.get('ciudad')
                    codigo_postal = form.cleaned_data.get('codigo_postal')

                    direccion = Direccion(
                        user=self.request.user,
                        nombre_referencia = nombre_referencia,
                        telefono=telefono,
                        direccion_especifica=direccion_especifica,
                        pais=pais,
                        provincia=provincia,
                        cuidad=ciudad,
                        codigo_postal=codigo_postal,
                        default=False
                    )
                    direccion.save()
                    pedido.direccion_envio = direccion
                    pedido.save()
                    guardar = form.cleaned_data.get('guardar')
                    if guardar:
                        direccion.default=True
                        direccion.save()

                    return redirect("core:pago")



        except Exception as e:
            print(e)
            return redirect("core:verificar")



    """def post(self, *args, **kwargs):
        form = DireccionForm(self.request.POST or None)
        try:
            print(form.errors)
            pedido = Pedido.objects.get(user=self.request.user, ordenado=False)
            if form.is_valid():
                default = form.cleaned_data.get('default')
                if default:
                    verificar = Direccion.objects.get(
                        user=self.request.user,
                        default = True
                    )
                    print(verificar)
                    if verificar.exists():
                        print("4")
                        direccion = verificar[0]
                        pedido.direccion_envio = direccion
                        pedido.save()
                        return redirect("core:inicio")
                    else:
                        print("5")

                else:
                    nombre_referencia = form.cleaned_data.get('nombre_referencia')
                    telefono = form.cleaned_data.get('telefono')
                    direccion_especifica = form.cleaned_data.get('direccion_especifica')
                   
                    pais = form.cleaned_data.get('pais')
                    provincia = form.cleaned_data.get('provincia')
                    ciudad = form.cleaned_data.get('ciudad')
                    codigo_postal = form.cleaned_data.get('codigo_postal')
                    default = form.cleaned_data.get('default')
                    print("6")
                    if campos_validados([nombre_referencia, telefono, direccion_especifica, provincia,
                                         ciudad, codigo_postal]):
                        print("7")
                        direccion = Direccion(
                            user=self.request.user,
                            nombre_referencia=nombre_referencia,
                            telefono=telefono,
                            direccion_especifica=direccion_especifica,
                            pais=pais,
                            provincia=provincia,
                            cuidad=ciudad,
                            codigo_postal=codigo_postal,
                            default=False
                        )
                        direccion.save()
                        pedido.direccion_especifica = direccion
                        pedido.save()
                        print("s   wwqewqewqewqewqewe")
                        if default:
                            direccion.default = True
                            direccion.save()

                        return redirect("core:inicio")
        except Exception as e:
            print(e)
            return redirect('core:verificar')"""

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