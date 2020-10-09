from django.db import models
from django.urls import reverse
from django.conf import settings
from django_countries.fields  import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from sorl.thumbnail import ImageField, get_thumbnail
from PIL import Image

# Create your models here.

position_choices = (
    ("C","Centro"),
    ("D", "Derecha")
)


class Categorias(models.Model):
    imagen_referencia = ImageField(upload_to='media/categorias', blank=True, null=True)
    nombre = models.CharField(max_length=100, default="Sin categoria")
    descripcion = models.CharField(max_length=100, default="Sin descripcion")
    color_descriptivo = models.CharField(max_length=9, default="black")

    def __str__(self):
        return self.nombre


class Slider(models.Model):
    image = models.ImageField(upload_to="media")
    texto = models.TextField(max_length=500)
    texto_pequeño = models.TextField(max_length=500)
    posicion = models.CharField(max_length=1, choices=position_choices)

class Articulo(models.Model):
    nombre = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    imagen_presentacion = models.ImageField(upload_to="media", null=True)
    descripcion = models.TextField(max_length=500)
    imagen_referencia = models.ManyToManyField("ImagenRefencia")
    precio = models.FloatField(default=0.00)
    descuento = models.FloatField(default=0.00)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        
        return reverse('core:producto', kwargs={'pk': self.pk})

    def add_to_cart(self):
        return reverse('core:add_to_cart',
                        kwargs={'pk':self.pk}
        )

   
class ArticuloPedido(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    ordenado = models.BooleanField(default=False)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return "{} de {}".format(self.cantidad, self.articulo)

    def subtotal_precio(self):
        return self.cantidad * self.articulo.precio

    def descuento(self):
        return self.cantidad * self.articulo.descuento

    def total_con_descuento(self):
        return self.subtotal_precio() - self.descuento()

    def total(self):
        if self.articulo.descuento:
            return self.total_con_descuento()
        else:
            return self.subtotal_precio()


class Pedido(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE
                            )
    articulos_pedidos= models.ManyToManyField(ArticuloPedido)
    fecha_inicio = models.DateTimeField(auto_now=True)
    fecha_pedido = models.DateTimeField()
    direccion_envio = models.ForeignKey('Direccion', on_delete=models.SET_NULL, blank=True, null=True)
    ordenado = models.BooleanField(default=False)
    entregado = models.BooleanField(default=False)
    pago = models.ForeignKey('Pago', on_delete=models.SET_NULL, blank=True, null=True)

    def total_pagar(self):
        total = 0
        for articulo in self.articulos_pedidos.all():
            total +=  articulo.total()
        return total


class ImagenRefencia(models.Model):
   
    imagen = models.ImageField(upload_to="media")
    descripcion = models.TextField(max_length=50, null=True, blank=True)


class Direccion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE
                        )
    nombre_referencia = models.CharField(max_length=100)
    telefono = PhoneNumberField(blank=True, help_text='Numero de contacto')
    direccion_especifica = models.CharField(max_length=50)
    pais = CountryField(multiple=False)
    provincia = models.CharField(max_length=50)
    cuidad = models.CharField(max_length=50)
    codigo_postal = models.IntegerField()
    default = models.BooleanField(default=False)
    

    def __str__(self):
        return self.user.username
    

class Pago(models.Model):
    stripe_charger_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE
                            )
    total_pago = models.FloatField()
    timestap = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username