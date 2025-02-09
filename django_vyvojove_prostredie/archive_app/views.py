from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db import models
from .models import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Permission
from typing import Type, Optional, Dict, Any
from itertools import chain
from .forms import *


def get_all(model: Type[models.Model], filters: Optional[Dict[str, Any]] = None):
    if filters is None:
        filters = {}
    return model.objects.filter(**filters)

def main_page(request):
    return render(request, 'archive_app/index.html')

def list_plays(request):
    plays = get_all(Play)
    return render(request, 'archive_app/plays.html', {'plays':plays})

def list_concerts_and_events(request):
    concerts = get_all(Concert)
    return render(request, 'archive_app/concerts.html', {'concerts':concerts})

def list_ensembles(request):
    publicity = request.GET.get('publicity')
    sort_order = request.GET.get('sort_order')
    
    ensembles = Ensemble.objects.all()
    
    if publicity == "true":
        ensembles = ensembles.filter(publicity=True)
    elif publicity == "false":
        ensembles = ensembles.filter(publicity=False)
    
    if sort_order == "asc":
        ensembles = ensembles.order_by('name')
    elif sort_order == "desc":
        ensembles = ensembles.order_by('-name')
    
    return render(request, 'archive_app/ensembles.html', {
        'ensembles': ensembles,
        'selected_publicity': publicity,
        'selected_sort_order': sort_order,
    })
    
    #ensembles = get_all(Ensemble)
    #return render(request, 'archive_app/ensembles.html', {'ensembles':ensembles})

def list_employees(request):
    publicity = request.GET.get('publicity')
    if publicity == "true":
        employees = Employee.objects.filter(publicity=True)
    elif publicity == "false":
        employees = Employee.objects.filter(publicity=False)
    else:
        employees = Employee.objects.all()
        #employees = get_all(Employee)
    return render(request, 'archive_app/employees.html', {'employees': employees})
    '''
    publicity = request.GET.get('publicity')
    first_name = request.GET.get('first_name')
    sort_order = request.GET.get('sort_order')
    ensemble_id = request.GET.get('ensemble')
    job_id = request.GET.get('job')
    key_term = request.GET.get('key_term')
    
    employees = Employee.objects.all()
    
    if publicity == "true":
        employees = employees.filter(publicity=True)
    elif publicity == "false":
        employees = employees.filter(publicity=False)
    
    if first_name and first_name != "-":
        employees = employees.filter(first_name=first_name)
    
    if ensemble_id and ensemble_id != "-":
        employees = employees.filter(ensemble_id=ensemble_id)
    
    if job_id and job_id != "-":
        employees = employees.filter(employeejob__job_id=job_id)
    
    if key_term:
        employees = employees.filter(description__icontains=key_term)
    
    if sort_order == "asc":
        employees = employees.order_by('last_name')
    elif sort_order == "desc":
        employees = employees.order_by('-last_name')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        employees_data = list(employees.values('id', 'first_name', 'last_name'))
        return JsonResponse(employees_data, safe=False)
    
    first_names = Employee.objects.values_list('first_name', flat=True).distinct()
    ensembles = Ensemble.objects.all()
    jobs = Job.objects.all()
    
    return render(request, 'archive_app/employees.html', {
        'employees': employees,
        'first_names': first_names,
        'ensembles': ensembles,
        'jobs': jobs,
    })'''

def form_plays(request):
    genres = GenreType.objects.all()
    ensembles = Ensemble.objects.all()
    if request.method == 'POST':
        print("AAAAAAAAA:", request.POST)
        form = PlayForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_plays')  # Redirect to a view that lists employees
        else:
            print(form.errors)
    else:
        form = PlayForm()
    return render(request,'archive_app/form_play.html', {
        'form':form, 'genres':genres, 'ensembles':ensembles
    })

def form_repeats(request, id):
    play = get_object_or_404(Play, pk=id)
    return render(request,'archive_app/form_repeat.html', {'play':play})

def form_concerts_and_events(request):
    return render(request, 'archive_app/form_concerts_and_events.html')

def form_ensembles(request):
    return render(request,'archive_app/form_ensemble.html')


def form_employees(request): #virtualmachine44
    if request.method == 'POST':
        print("POST DATA:", request.POST)

        employee_form = EmployeeForm(request.POST)
        job_formset = EmployeeJobFormSet(request.POST)

        if employee_form.is_valid() and job_formset.is_valid():
            employee = employee_form.save()

            job_formset.instance = employee  # Assign employee to job formset
            job_formset.save()  # Save EmployeeJob instances

            return redirect('employee_list')  # Redirect after saving
        else:
            print("Form Errors:", employee_form.errors)
            print("Job Formset Errors:", job_formset.errors)
    else:
        employee_form = EmployeeForm()
        job_formset = EmployeeJobFormSet()

    return render(request, 'archive_app/form_employee.html', {
        'employee_form': employee_form,
        'job_formset': job_formset,
    })


def get_play(request, id):
    play = get_object_or_404(Play, pk=id)
    repeats = Repeat.objects.filter(play=play)

    # production = PlayPerformer.objects.filter(play=play)
    qs_roles = PlayPerformer.objects.filter(play=play)
    production = dict()
    for rp in qs_roles:
        job = rp.employee_job.job
        employee = rp.employee
        if job not in production:
            production[job] = []
        production[job].append(employee)

    qs = RepeatPerformer.objects.filter(repeat__in=repeats)
    performers = dict()
    for rp in qs:
        job = rp.employee_job.job
        employee = rp.employee_job.employee
        if job not in performers:
            performers[job] = []
        performers[job].append(employee)

    return render(request, 'archive_app/get_play.html', {
        'play': play, 'repeats':repeats, 'production':production, 'performers':performers
    })

def get_repeat(request, id_play, id_repeat):
    play = get_object_or_404(Play, pk=id_play)
    repeat = get_object_or_404(Repeat, pk=id_repeat)

    qs = RepeatPerformer.objects.filter(repeat=repeat)
    performers = dict()
    for rp in qs:
        job = rp.employee_job.job
        employee = rp.employee_job.employee
        if job not in performers:
            performers[job] = []
        performers[job].append(employee)

    return render(request, 'archive_app/get_repeat.html', {
        'play': play, 'repeat':repeat, 'performers':performers
    })

def get_concert_or_event(request, id_concert):
    concert = get_object_or_404(Concert, pk=id_concert)

    qs = ConcertPerformer.objects.filter(concert=concert)
    production = dict()
    for rp in qs:
        job = rp.job
        employee = rp.employee
        if job not in production:
            production[job] = []
        production[job].append(employee)

    return render(request, 'archive_app/get_concert.html', {
        'concert': concert, 'production':production
    })

def get_ensemble(request, id):
    ensemble = get_object_or_404(Ensemble, pk=id)
    qs = Employee.objects.filter(ensemble=ensemble)

    return render(request, 'archive_app/get_ensemble.html', {
        'ensemble': ensemble, 'people': qs
    })

def get_employee(request, id):
    employee = get_object_or_404(Employee, pk=id)

    roles = EmployeeJob.objects.filter(employee=employee)

    # if in production
    productions = Play.objects.filter(
        playperformer__employee_job__employee=employee
    ).distinct().order_by('title')

    # if in play
    plays = Play.objects.filter(
        repeat__repeatperformer__employee_job__employee=employee
    ).distinct().order_by('title')

    plays = list(chain(plays, productions))

    concerts = Concert.objects.filter(
        concertperformer__employee=employee
    ).distinct().order_by('name')

    return render(request, 'archive_app/get_employee.html', {
        'employee':employee, 'plays':plays , 'concerts':concerts, 'roles':roles
    })

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
    error_message = None
    success_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        real_name = request.POST.get('real_name')
        your_password = request.POST.get('your_password')

        if not username or not email or not password or not confirm_password or not real_name or not your_password:
            error_message = 'Všetky polia musia byť vyplnené.'
        elif password != confirm_password:
            error_message = 'Heslá sa nezhodujú.'
        elif not request.user.check_password(your_password):
            error_message = 'Vaše heslo je nesprávne.'
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_staff = True
                user.save()
                permissions = Permission.objects.all()
                user.user_permissions.set(permissions)

                UserProfile.objects.create(user=user, real_name=real_name)

                success_message = f'Používateľ {username} bol úspešne pridaný ako administrátor.'
                return redirect('create_admin')

            except Exception as e:
                error_message = f'Chyba pri vytváraní používateľa: {str(e)}'

    users_profiles = enumerate(
        [(user, UserProfile.objects.filter(user=user).first()) for user in User.objects.order_by('id')],
        start=1
    )

    return render(request, 'archive_app/create_admin.html', {
        'error': error_message,
        'success': success_message,
        'users_profiles': users_profiles,
    })

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    error_message = None
    success_message = None
    if request.method == 'POST':
        try:
            user_to_delete = get_object_or_404(User, id=user_id)
            if user_to_delete.is_superuser and User.objects.filter(is_superuser=True).count() == 1:
                error_message = 'Nemôžete odstrániť hlavného superusera. Aspoň jeden superuser musí zostať.'
            elif user_to_delete == request.user:
                error_message = 'Nemôžete odstrániť účet, pod ktorým ste prihlásený.'
            else:
                user_to_delete.delete()
                success_message = f'Používateľ {user_to_delete.username} bol úspešne odstránený.'
                return redirect('create_admin')
        except Exception as e:
            error_message = f'Chyba pri odstraňovaní používateľa: {str(e)}'
    users_profiles = enumerate(
        [(user, UserProfile.objects.filter(user=user).first()) for user in User.objects.order_by('id')],
        start=1
    )
    return render(request, 'archive_app/create_admin.html', {
        'error': error_message,
        'success': success_message,
        'users_profiles': users_profiles,
    })