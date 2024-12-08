from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(response):
    return HttpResponse("<h1>test</h1>")

def empty_page(request):
    return render(request, 'empty_page.html')