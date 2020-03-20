from django.shortcuts import render
from django.views import View
from django.utils.http import http_date

# Create your views here.

class Inicio(View):
    def get(self, request):
        return render (self.request, "index.html")