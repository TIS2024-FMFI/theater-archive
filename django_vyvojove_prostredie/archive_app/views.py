from operator import truediv

from django.forms.formsets import TOTAL_FORM_COUNT, INITIAL_FORM_COUNT
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
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
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Q
from datetime import datetime


def get_all(model: Type[models.Model], filters: Optional[Dict[str, Any]] = None):
    if filters is None:
        filters = {}
    return model.objects.filter(**filters)

def autocomplete(request, model):
    if request.GET.get('q'):
        q = request.GET['q']
        data = model.objects.using('legacy').filter(email__startswith=q).values_list('email',flat=True)
        json = list(data)
        return JsonResponse(json, safe=False)
    else:
        HttpResponse("No cookies")

def main_page(request):
    return render(request, 'archive_app/index.html')

def list_plays(request):
    genre = request.GET.get('genre')
    ensemble = request.GET.get('ensemble')
    season = request.GET.get('season')
    publicity = request.GET.get('publicity')
    sort_order = request.GET.get('sort_order')
    search = request.GET.get('search')

    plays = Play.objects.all()
    
    if genre and genre != "-":
        plays = plays.filter(genre_type_id=genre)
    
    if ensemble and ensemble != "-":
        plays = plays.filter(ensemble_id=ensemble)
    
    if season and season != "-":
        # month, year = season.split('-')
        # plays = plays.filter(repeat__date__month=month, repeat__date__year=year)
        start_year, end_year = map(int, season.split('/'))
        start_date = f"{start_year}-07-01"
        end_date = f"{end_year}-06-30"
        plays = plays.filter(repeat__date__range=[start_date, end_date]).distinct()


    if search and search != "":
        plays = plays.filter(Q(title__icontains=search) |
                             Q(author_first_name__icontains=search) |
                             Q(author_last_name__icontains=search))

    if not request.user.is_authenticated:
        plays = plays.filter(publicity=True)  # only public employees if not logged in
    elif publicity == "true":
        plays = plays.filter(publicity=True)
    elif publicity == "false":
        plays = plays.filter(publicity=False)
    
    if sort_order == "asc":
        plays = plays.order_by('title')
    elif sort_order == "desc":
        plays = plays.order_by('-title')
    
    genres = GenreType.objects.all()
    ensembles = Ensemble.objects.all()
    # seasons = Repeat.objects.annotate(month=TruncMonth('date'), year=TruncYear('date')).values_list('month', 'year').distinct()
    start_year = 1920
    current_year = datetime.now().year
    seasons = [(f"{year}/{year + 1}") for year in range(start_year, current_year)]

    return render(request, 'archive_app/plays.html', {
        'plays': plays,
        'genres': genres,
        'ensembles': ensembles,
        'seasons': seasons,
        'selected_genre': genre,
        'selected_ensemble': ensemble,
        'selected_season': season,
        'selected_publicity': publicity,
        'selected_sort_order': sort_order,
        'selected_search': search,
    })

def list_concerts_and_events(request):
    publicity = request.GET.get('publicity')
    concert_type_id = request.GET.get('concert_type')
    sort_order = request.GET.get('sort_order')
    search = request.GET.get('search')

    concerts = Concert.objects.all()


    if not request.user.is_authenticated:
        concerts = concerts.filter(publicity=True)  # only public employees if not logged in
    elif publicity == "true":
        concerts = concerts.filter(publicity=True)
    elif publicity == "false":
        concerts = concerts.filter(publicity=False)
    
    if concert_type_id:
        concerts = concerts.filter(concert_type_id=concert_type_id)

    if search and search != "":
        concerts = concerts.filter(name__icontains=search)

    if sort_order == "asc":
        concerts = concerts.order_by('name')
    elif sort_order == "desc":
        concerts = concerts.order_by('-name')
    
    concert_types = ConcertType.objects.all()
    
    return render(request, 'archive_app/concerts.html', {
        'concerts': concerts,
        'concert_types': concert_types,
        'selected_publicity': publicity,
        'selected_concert_type': concert_type_id,
        'selected_sort_order': sort_order,
        'selected_search': search,
    })
    #concerts = get_all(Concert)
    #return render(request, 'archive_app/concerts.html', {'concerts':concerts})

def list_ensembles(request):
    publicity = request.GET.get('publicity')
    sort_order = request.GET.get('sort_order')
    search = request.GET.get('search')

    ensembles = Ensemble.objects.all()

    if not request.user.is_authenticated:
        ensembles = ensembles.filter(publicity=True)  # only public employees if not logged in
    elif publicity == "true":
        ensembles = ensembles.filter(publicity=True)
    elif publicity == "false":
        ensembles = ensembles.filter(publicity=False)

    if search and search != "":
        ensembles = ensembles.filter(name__icontains=search)

    if sort_order == "asc":
        ensembles = ensembles.order_by('name')
    elif sort_order == "desc":
        ensembles = ensembles.order_by('-name')
    
    return render(request, 'archive_app/ensembles.html', {
        'ensembles': ensembles,
        'selected_publicity': publicity,
        'selected_sort_order': sort_order,
        'selected_search': search,
    })
    
    #ensembles = get_all(Ensemble)
    #return render(request, 'archive_app/ensembles.html', {'ensembles':ensembles})

def list_employees(request):
    publicity = request.GET.get('publicity')
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    role = request.GET.get('role')
    sort_order = request.GET.get('sort_order')

    search = request.GET.get('search')

    employees = Employee.objects.all()
    
    if not request.user.is_authenticated:
        employees = employees.filter(publicity=True)  # only public employees if not logged in

    elif publicity == "true":
        employees = employees.filter(publicity=True)
    elif publicity == "false":
        employees = employees.filter(publicity=False)
    
    if first_name and first_name != "-":
        employees = employees.filter(first_name=first_name)
    
    if last_name and last_name != "-":
        employees = employees.filter(last_name=last_name)
    
    if role and role != "-":
        employees = employees.filter(employeejob__job__name=role)

    if search and search != "":
        employees = employees.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search))

    if sort_order == "asc":
        employees = employees.order_by('last_name')
    elif sort_order == "desc":
        employees = employees.order_by('-last_name')
    
    first_names = Employee.objects.values_list('first_name', flat=True).distinct()
    last_names = Employee.objects.values_list('last_name', flat=True).distinct()
    roles = EmployeeJob.objects.filter(job__play_character=False).values_list('job__name', flat=True).distinct()
    
    return render(request, 'archive_app/employees.html', {
        'employees': employees,
        'first_names': first_names,
        'last_names': last_names,
        'roles': roles,
        'selected_publicity': publicity,
        'selected_first_name': first_name,
        'selected_last_name': last_name,
        'selected_role': role,
        'selected_sort_order': sort_order,
        'selected_search': search
    })



def form_plays(request):
    genres = GenreType.objects.all()
    ensembles = Ensemble.objects.all()
    if request.method == 'POST':
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
    RepeatPerformerFormSet = inlineformset_factory(
        Repeat, RepeatPerformer,
        form=RepeatPerformerForm,
        extra=1,  # Allow adding at least one performer
        can_delete=True  # Allow deleting performers
    )

    play = get_object_or_404(Play, pk=id)

    if request.method == 'POST':
        print("POST data:", request.POST)
        repeat_form = RepeatForm(request.POST)
        performer_formset = RepeatPerformerFormSet(request.POST)


        if repeat_form.is_valid() and performer_formset.is_valid():
            repeat = repeat_form.save(commit=False)
            repeat.play = play
            repeat.save()

            performers = performer_formset.save(commit=False)
            for performer in performers:
                performer.repeat = repeat
                performer.save()  # This automatically assigns EmployeeJob

            return redirect('get_repeat', id_play=play.id, id_repeat=repeat.id)  # Redirect after saving

        else:
            print("Repeat Errors:", repeat_form.errors)
            print("Performer Formset Errors:", performer_formset.errors)
    else:
        repeat_form = RepeatForm()
        performer_formset = RepeatPerformerFormSet()

    return render(request, 'archive_app/form_repeat.html', {
        'play': play,
        'repeat_form': repeat_form,
        'performer_formset': performer_formset
    })

def form_concerts_and_events(request):
    ConcertPerformerFormSet = inlineformset_factory(
        Concert, ConcertPerformer,
        form=ConcertPerformerForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        print("POST data:", request.POST)
        concert_form = ConcertForm(request.POST)
        performer_formset = ConcertPerformerFormSet(request.POST)

        if (concert_form.is_valid() and performer_formset.is_valid()):
            concert = concert_form.save()

            performers = performer_formset.save(commit=False)
            for performer in performers:
                performer.concert = concert
                performer.save()  # This automatically assigns EmployeeJob

            return redirect('get_concert_or_event', id_concert=concert.id)  # Redirect to a list of concerts or another appropriate view

        else:
            print(concert_form.errors)
            print(performer_formset.errors)
    else:
        concert_form = ConcertForm()
        performer_formset = ConcertPerformerFormSet()

    return render(request, 'archive_app/form_concerts_and_events.html', {
        'concert_form': concert_form,
        'performer_formset': performer_formset
    })

def form_ensembles(request):
    if request.method == "POST":
        form = EnsembleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_ensembles')  # Redirect to the list of ensembles after saving
    else:
        form = EnsembleForm()
    
    return render(request, 'archive_app/form_ensemble.html', {'form': form})
    #return render(request,'archive_app/form_ensemble.html')


def form_employees(request): #virtualmachine44
    EmployeeJobFormSet = inlineformset_factory(
        Employee, EmployeeJob,
        form=EmployeeJobForm,
        extra=1
        # can_delete=True
    )

    if request.method == 'POST':
        print("POST DATA:", request.POST)

        employee_form = EmployeeForm(request.POST)
        job_formset = EmployeeJobFormSet(request.POST)

        if employee_form.is_valid() and job_formset.is_valid():
            employee = employee_form.save()

            job_formset.instance = employee  # Assign employee to job formset
            job_formset.save()  # Save EmployeeJob instances

            return redirect('list_employees')  # Redirect after saving
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
    if not request.user.is_authenticated:
        repeats = Repeat.objects.filter(play=play, publicity=True)
    else:
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
        if employee not in performers[job]:
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
        if employee not in performers[job]:
            performers[job].append(employee)

    return render(request, 'archive_app/get_repeat.html', {
        'play': play, 'repeat':repeat, 'performers':performers
    })

def get_concert_or_event(request, id_concert):
    concert = get_object_or_404(Concert, pk=id_concert)
    concert_documents = ConcertDocument.objects.filter(concert=concert)
    #program_documents = concert_documents.filter(document__file__endswith='.pdf')

    qs = ConcertPerformer.objects.filter(concert=concert)
    production = dict()
    for rp in qs:
        job = rp.job
        employee = rp.employee
        if job not in production:
            production[job] = []
        production[job].append(employee)

    return render(request, 'archive_app/get_concert.html', {
        'concert': concert,
        'production':production,
        #'program_documents': program_documents,
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


def edit_ensemble(request, ensemble_id):
    ensemble = get_object_or_404(Ensemble, id=ensemble_id)
    
    if request.method == "POST":
        form = EnsembleForm(request.POST, instance=ensemble)
        if form.is_valid():
            form.save()
            print("Form is valid and saved")
            return redirect('get_ensemble', id=ensemble.id)
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = EnsembleForm(instance=ensemble)
        
    return render(request, 'archive_app/form_ensemble.html', {'form': form, 'ensemble': ensemble})


def copy_ensemble(request, ensemble_id):
    original_ensemble = get_object_or_404(Ensemble, id=ensemble_id)
    
    if request.method == "POST":
        form = EnsembleForm(request.POST)
        if form.is_valid():
            new_ensemble = form.save(commit=False)
            if new_ensemble.name == original_ensemble.name:
                form.add_error('name', 'The name must be different from the original ensemble.')
            elif Ensemble.objects.filter(name=new_ensemble.name).exists():
                form.add_error('name', 'An ensemble with this name already exists.')
            else:
                new_ensemble.save()
                return redirect('get_ensemble', id=new_ensemble.id)
    else:
        form = EnsembleForm(instance=original_ensemble)
        form.initial['name'] = ''  # Clear the name field to force the user to enter a new name
    
    return render(request, 'archive_app/form_ensemble.html', {'form': form, 'ensemble': original_ensemble})
    
def edit_employee(request, id):
    EmployeeJobFormSet = inlineformset_factory(
        Employee, EmployeeJob,
        form=EmployeeJobForm,
        extra=0,
        can_delete=True
    )

    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST, instance=employee)
        job_formset = EmployeeJobFormSet(request.POST, instance=employee)

        if employee_form.is_valid() and job_formset.is_valid():
            print("POST Data:", request.POST)
            employee_form.save()

            return redirect('list_employees')  # Redirect after saving
        else:
            print("Form Errors:", employee_form.errors)
            print("Job Formset Errors:", job_formset.errors)
    else:
        employee_form = EmployeeForm(instance=employee)
        job_formset = EmployeeJobFormSet(instance=employee)

    return render(request, 'archive_app/form_employee.html', {
        'employee_form': employee_form,
        'job_formset': job_formset,
        'employee': employee
    })


def edit_play(request, id):
    genres = GenreType.objects.all()
    ensembles = Ensemble.objects.all()
    play = get_object_or_404(Play, id=id)

    if request.method == 'POST':
        form = PlayForm(request.POST, instance=play)
        if form.is_valid():
            form.save()
            return redirect('list_plays')  # Redirect to a view that lists employees
        else:
            print(form.errors)
    else:
        form = PlayForm(instance=play)
    return render(request, 'archive_app/form_play.html', {
        'form': form, 'genres': genres, 'ensembles': ensembles, 'play':play
    })


def edit_repeat(request, id_play, id_repeat):
    RepeatPerformerFormSet = inlineformset_factory(
        Repeat, RepeatPerformer,
        form=RepeatPerformerForm,
        extra=0,
        can_delete=True
    )

    repeat = get_object_or_404(Repeat, id=id_repeat)
    play = get_object_or_404(Play, pk=id_play)

    if request.method == 'POST':
        print("POST data:", request.POST)

        repeat_form = RepeatForm(request.POST, instance=repeat)
        performer_formset = RepeatPerformerFormSet(request.POST, instance=repeat)

        if repeat_form.is_valid() and performer_formset.is_valid():
            # repeat = repeat_form.save(commit=False)
            # repeat.play = play
            repeat.save()

            # performers = performer_formset.save(commit=False)
            for form in performer_formset:
                if form.cleaned_data.get("DELETE", False):
                    if form.instance.pk:
                        form.instance.delete()
                else:
                    form.save()

            return redirect('get_repeat', id_play=play.id, id_repeat=repeat.id)  # Redirect after saving

        else:
            print("Repeat Errors:", repeat_form.errors)
            print("Performer Formset Errors:", performer_formset.errors)
    else:

        repeat_form = RepeatForm(instance=repeat)
        performer_formset = RepeatPerformerFormSet(instance=repeat)

    return render(request, 'archive_app/form_repeat.html', {
        'play': play,
        'repeat': repeat,
        'repeat_form': repeat_form,
        'performer_formset': performer_formset
    })


def edit_concert(request, concert_id):
    ConcertPerformerFormSet = inlineformset_factory(
        Concert, ConcertPerformer,
        form=ConcertPerformerForm,
        extra=1,
        can_delete=True
    )
    concert = get_object_or_404(Concert, id=concert_id)

    if request.method == 'POST':
        print(request.POST)
        concert_form = ConcertForm(request.POST, instance=concert)
        performer_formset = ConcertPerformerFormSet(request.POST, instance=concert)

        if concert_form.is_valid() and performer_formset.is_valid():
            concert = concert_form.save()

            for performer in performer_formset:
                if performer.cleaned_data.get("DELETE", False):
                    if performer.instance.pk:
                        performer.instance.delete()
                else:
                    if performer.cleaned_data.get('employee_name') and performer.cleaned_data.get('job'):
                        performer.concert = concert
                        performer.save()  # This automatically assigns EmployeeJob

            return redirect('get_concert_or_event', id_concert=concert.id)
        else:
            print(concert_form.errors)
            print(performer_formset.errors)

    else:
        concert_form = ConcertForm(instance=concert)
        performer_formset = ConcertPerformerFormSet(instance=concert)



    return render(request, 'archive_app/form_concerts_and_events.html', {
        'concert_form': concert_form,
        'concert': concert,
        'performer_formset': performer_formset
    })


def copy_concert(request, concert_id):
    ConcertPerformerFormSet = inlineformset_factory(
        Concert, ConcertPerformer,
        form=ConcertPerformerForm,
        extra=1,
        can_delete=True
    )

    concert = get_object_or_404(Concert, id=concert_id)

    if request.method == 'POST':
        print(request.POST)
        concert_form = ConcertForm(request.POST)
        performer_formset = ConcertPerformerFormSet(request.POST, instance=concert)

        if concert_form.is_valid() and performer_formset.is_valid():
            new_concert = concert_form.save(commit=False)
            new_concert.id = None  # Ensure a new entry is created
            new_concert.save()

            performers = performer_formset.save(commit=False)
            for performer in performers:
                performer.concert = new_concert
                performer.save()  # This automatically assigns EmployeeJob

            return redirect('get_concert_or_event',
                            id_concert=new_concert.id)  # Redirect to the new concert detail view after saving
        else:
            print(concert_form.errors)
            print(performer_formset.errors)

    else:
        concert_form = ConcertForm(instance=concert)
        concert_form.fields['name'].initial = ''
        performer_formset = ConcertPerformerFormSet(instance=concert)


    return render(request, 'archive_app/form_concerts_and_events.html', {
        'concert_form': concert_form,
        'concert': concert,
        'performer_formset': performer_formset

    })

def copy_play(request, id):
    genres = GenreType.objects.all()
    ensembles = Ensemble.objects.all()
    play = get_object_or_404(Play, id=id)

    if request.method == 'POST':
        form = PlayForm(request.POST, instance=play)
        if form.is_valid():
            new_play = form.save(commit=False)
            new_play.id = None
            new_play.save()
            return redirect('get_play', id=new_play.id)  # Redirect to a view that lists employees
        else:
            print(form.errors)
    else:
        form = PlayForm(instance=play)
    return render(request, 'archive_app/form_play.html', {
        'form': form, 'genres': genres, 'ensembles': ensembles, 'play':play
    })


def copy_repeat(request, id_play, id_repeat):
    RepeatPerformerFormSet = inlineformset_factory(
        Repeat, RepeatPerformer,
        form=RepeatPerformerForm,
        extra=0,
        can_delete=True
    )

    repeat = get_object_or_404(Repeat, id=id_repeat)
    play = get_object_or_404(Play, pk=id_play)

    if request.method == 'POST':
        print("POST data:", request.POST)

        repeat_form = RepeatForm(request.POST, instance=repeat)
        performer_formset = RepeatPerformerFormSet(request.POST, instance=repeat)

        if repeat_form.is_valid() and performer_formset.is_valid():
            new_repeat = repeat_form.save(commit=False)
            new_repeat.play = play
            new_repeat.id = None
            new_repeat.save()

            # performers = performer_formset.save(commit=False)
            performers = performer_formset.save(commit=False)
            for performer in performers:
                performer.repeat = new_repeat
                performer.save()

            return redirect('get_repeat', id_play=play.id, id_repeat=new_repeat.id)  # Redirect after saving

        else:
            print("Repeat Errors:", repeat_form.errors)
            print("Performer Formset Errors:", performer_formset.errors)
    else:

        repeat_form = RepeatForm(instance=repeat)
        performer_formset = RepeatPerformerFormSet(instance=repeat)

    return render(request, 'archive_app/form_repeat.html', {
        'play': play,
        'repeat': repeat,
        'repeat_form': repeat_form,
        'performer_formset': performer_formset
    })


# def create_concert(request):
#     if request.method == 'POST':
#         concert_form = ConcertForm(request.POST)
#         director_form = ConcertPerformerForm(request.POST, prefix='director')
#         scene_form = ConcertPerformerForm(request.POST, prefix='scene')
#         dramaturgy_form = ConcertPerformerForm(request.POST, prefix='dramaturgy')
#         performer_forms = [ConcertPerformerForm(request.POST, prefix=str(i)) for i in range(0, int(request.POST['performer_count']))]
#         document_form = DocumentForm(request.POST, request.FILES)
#         performer_count = int(request.POST.get('performer_count', 1))

#         if concert_form.is_valid() and director_form.is_valid() and scene_form.is_valid() and dramaturgy_form.is_valid() and all([pf.is_valid() for pf in performer_forms]):
#             concert = concert_form.save()

#             # Does the job "Réžia" exist? If no, create it.
#             director_job, created = Job.objects.get_or_create(name="Réžia")
#             director = director_form.save(commit=False)
#             director.concert = concert
#             director.job = director_job
#             director.save()

#             scene_job, created = Job.objects.get_or_create(name="Scéna")
#             scene = scene_form.save(commit=False)
#             scene.concert = concert
#             scene.job = scene_job
#             scene.save()

#             dramaturgy_job, created = Job.objects.get_or_create(name="Dramaturg")
#             dramaturgy = dramaturgy_form.save(commit=False)
#             dramaturgy.concert = concert
#             dramaturgy.job = dramaturgy_job
#             dramaturgy.save()

#             for performer_form in performer_forms:
#                 performer = performer_form.save(commit=False)
#                 performer.concert = concert
#                 performer.save()

#             if document_form.is_valid():
#                 for file in request.FILES.getlist('program_files'):
#                     document = Document(file=file)
#                     document.save()
#                     ConcertDocument.objects.create(concert=concert, document=document)

#                 for file in request.FILES.getlist('photo_files'):
#                     document = Document(file=file)
#                     document.save()
#                     ConcertDocument.objects.create(concert=concert, document=document)

#             return redirect('concert_list')  # Redirect to a list of concerts or another appropriate view
#         else:
#             # debugging
#             print(concert_form.errors)
#             print(director_form.errors)
#             print(scene_form.errors)
#             print(dramaturgy_form.errors)
#             for pf in performer_forms:
#                 print(pf.errors)
#             print(document_form.errors)

#     else:
#         concert_form = ConcertForm()
#         director_form = ConcertPerformerForm(prefix='director')
#         scene_form = ConcertPerformerForm(prefix='scene')
#         dramaturgy_form = ConcertPerformerForm(prefix='dramaturgy')
#         performer_forms = [ConcertPerformerForm(prefix=str(i)) for i in range(1)]
#         document_form = DocumentForm()

#     employees = Employee.objects.all()
#     jobs = Job.objects.filter(play_character=False)

#     return render(request, 'archive_app/form_concerts_and_events.html', {
#         'concert_form': concert_form,
#         'director_form': director_form,
#         'scene_form': scene_form,
#         'dramaturgy_form': dramaturgy_form,
#         'performer_forms': performer_forms,
#         'document_form': document_form,
#         'employees': employees,
#         'jobs': jobs,
#     })


# def edit_concert(request, concert_id):
# concert = get_object_or_404(ConcertOrEvent, id=concert_id)