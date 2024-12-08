from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(response):
    return HttpResponse('''
            <h1>Welcome to the Home Page</h1>
            <button onclick="location.href='/second/'">Go to Second Page</button>
        ''')

def second_view(request):
    return HttpResponse('<h1>This is the second page</h1>')