from django.shortcuts import render
from django.views import View
from django.utils.http import http_date
from .models import Slider

# Create your views here.

class Inicio(View):
    def get(self, request):
        context = {
            "slider" : Slider.objects.all()
        }
        return render (self.request, "index.html", context)