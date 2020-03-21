from django.db import models

# Create your models here.
position_choices = (
    ("C","Centro"),
    ("D", "Derecha")
)
class Slider(models.Model):
    image = models.ImageField(upload_to="media")
    texto = models.TextField(max_length=500)
    texto_pequeño = models.TextField(max_length=500)
    posicion = models.CharField(max_length=1, choices=position_choices)


class Articulo(models.Model):
    nombre = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=500)
    imagen_referencia = models.ManyToManyField("ImagenRefencia")
    precio = models.FloatField()
    descuento = models.FloatField()

    def __str__(self):
        return self.nombre

class ImagenRefencia(models.Model):
    imagen = models.ImageField(upload_to="media")
    descripcion = models.TextField(max_length=50, null=True, blank=True)