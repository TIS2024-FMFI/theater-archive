from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def main_page(request):
    return render(request, 'archive_app/index.html')

def list_plays(request):
    return render(request, 'archive_app/plays.html')

def list_concerts_and_events(request):
    return HttpResponse('<h1>Tu budú vypísané koncerty a iné podujatia</h1>')

def list_ensembles(request):
    return HttpResponse('<h1>Tu budú vypísané súbory</h1>')

def list_employees(request):
    return HttpResponse('<h1>Tu budú vypísaní zamestnanci</h1>')

def form_plays(request):
    return HttpResponse('<h1>Toto bude formulár na pridanie nového predstavenia</h1>')

def form_repeats(request):
    return HttpResponse('<h1>Toto bude formulár na pridanie reprízy daného predstavenia</h1>')

def form_concerts_and_events(request):
    return HttpResponse('<h1>Toto bude formulár na pridanie nového koncertu alebo podujatia</h1>')

def form_ensembles(request):
    return HttpResponse('<h1>Toto bude formulár na pridanie nového súboru</h1>')

def form_employees(request):
    return HttpResponse('<h1>Toto bude formulár na pridanie nového zamestnanca</h1>')

def get_play(request):
    return HttpResponse('<h1>Tu budeme vidieť konkrétne predstavenie</h1>')

def get_repeat(request):
    return HttpResponse('<h1>Tu budeme vidieť konkrétnu reprízu daného predstavenia</h1>')

def get_concert_or_event(request):
    return HttpResponse('<h1>Tu budeme vidieť konkrétny koncert alebo predstavenie</h1>')

def get_ensemble(request):
    return HttpResponse('<h1>Tu budeme vidieť konkrétny súbor</h1>')

def get_employee(request):
    return HttpResponse('<h1>Tu budeme vidieť konkrétneho zamestnanca</h1>')

def admin_section(request):
    return HttpResponse('<h1>Tu sa budú spravovať ďalšie funkcionality administrátora</h1>')
