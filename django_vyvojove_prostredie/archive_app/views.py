from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import models
from .models import UserProfile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

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

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def create_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        real_name = request.POST.get('real_name')
        your_password = request.POST.get('your_password')

        if not username or not email or not password or not confirm_password or not real_name or not your_password:
            return render(request, 'archive_app/create_admin.html', {
                'error': 'Všetky polia musia byť vyplnené.',
                'users': User.objects.order_by('id'),
                'profiles': UserProfile.objects.all(),
            })
        
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'archive_app/create_admin.html', {
                'error': 'E-mail nie je platný.',
                'users_profiles': [(user, UserProfile.objects.filter(user=user).first()) for user in User.objects.order_by('id')],
            })
        if password != confirm_password:
            return render(request, 'archive_app/create_admin.html', {
                'error': 'Heslá sa nezhodujú.',
                'users_profiles': [(user, UserProfile.objects.filter(user=user).first()) for user in User.objects.order_by('id')],
            })
        if not request.user.check_password(your_password):
            return render(request, 'archive_app/create_admin.html', {
                'error': 'Vaše heslo je nesprávne.',
                'users_profiles': [(user, UserProfile.objects.filter(user=user).first()) for user in User.objects.order_by('id')],
            })
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = True
            user.save()

            UserProfile.objects.create(user=user, real_name=real_name)

            return redirect('create_admin')
        except Exception as e:
            return render(request, 'archive_app/create_admin.html', {
                'error': f'Chyba pri vytváraní administrátora: {str(e)}',
                'users_profiles': [(user, UserProfile.objects.filter(user=user).first()) for user in User.objects.order_by('id')],
            })

    return render(request, 'archive_app/create_admin.html', {
        'users_profiles': [(user, UserProfile.objects.filter(user=user).first()) for user in User.objects.order_by('id')],
    })

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    if request.method == 'POST':
        user_to_delete = get_object_or_404(User, id=user_id)
        if user_to_delete == request.user:
            return render(request, 'archive_app/create_admin.html', {
                'error': 'Nemôžete odstrániť účet, pod ktorým ste prihlásený.',
                'users_profiles': [(user, UserProfile.objects.filter(user=user).first()) for user in User.objects.order_by('id')],
            })
        if not user_to_delete.is_superuser:
            user_to_delete.delete()
    return redirect('create_admin')