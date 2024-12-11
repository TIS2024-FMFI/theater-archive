from django.urls import path
from . import views

urlpatterns = [
    path("", views.main_page, name = "main_page"),
    path('plays/', views.list_plays, name='list_plays'),
    path('concerts_and_events/', views.list_concerts_and_events, name='list_concerts_and_events'),
    path('ensembles/', views.list_ensembles, name='list_ensembles'),
    path('employees/', views.list_employees, name='list_employees'),
    path('plays/add_play/', views.form_plays, name='form_plays'),
    path('plays/get_play/add_repeat/', views.form_repeats, name='form_repeats'),
    path('concerts_and_events/add_concert_or_event/', views.form_concerts_and_events, name='form_concerts_and_events'),
    path('ensembles/add_ensemble/', views.form_ensembles, name='form_ensembles'),
    path('employees/add_employee/', views.form_employees, name='form_employees'),
    path('plays/get_play/', views.get_play, name='get_play'),
    path('plays/get_play/get_repeat/', views.get_repeat, name='get_repeat'),
    path('concerts_and_events/get_concert_or_event/', views.get_concert_or_event, name='get_concert_or_event'),
    path('ensembles/get_ensemble/', views.get_ensemble, name='get_ensemble'),
    path('employees/get_employee/', views.get_employee, name='get_employee'),
    path('admin_section/', views.admin_section, name='admin_section'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]