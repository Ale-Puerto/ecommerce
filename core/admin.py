from django.contrib import admin
from .models import (Slider,
                    Articulo,
                    ImagenRefencia,
                    Categorias
                    )

admin.site.register(Slider)
admin.site.register(Articulo)
admin.site.register(ImagenRefencia)
admin.site.register(Categorias)