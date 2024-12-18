from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def main_page(request):
    return render(request, 'archive_app/index.html')

def list_plays(request):
    return render(request, 'archive_app/plays.html')

def list_concerts_and_events(request):
    return render(request, 'archive_app/concerts.html')

def list_ensembles(request):
    return render(request, 'archive_app/ensembles.html')

def list_employees(request):
    return render(request, 'archive_app/employees.html')

def form_plays(request):
    return render(request,'archive_app/form_play.html')

def form_repeats(request):
    return HttpResponse('<h1>Toto bude formulár na pridanie reprízy daného predstavenia</h1>')

def form_concerts_and_events(request):
    return render(request, 'archive_app/form_concerts_and_events.html')

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

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('main_page')
            else:
                return render(request, 'archive_app/login.html', {'error': 'Nemáte administrátorské práva.'})
        else:
            return render(request, 'archive_app/login.html', {'error': 'Neplatné údaje.'})
    else:
        return render(request, 'archive_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('main_page')