from django.db import models

# Create your models here.

class Slider(models.Model):
    image = models.ImageField()
    texto = models.TextField(max_length=500)
    texto_pequeño = models.TextField(max_length=500)


    