from django.urls import path
from . import views

urlpatterns = [
    path("", views.main_page, name = "main_page"),
    path('plays/', views.list_plays, name='list_plays'),
    path('concerts_and_events/', views.list_concerts_and_events, name='list_concerts_and_events'),
    
    path('employees/', views.list_employees, name='list_employees'),
    path('plays/add_play/', views.form_plays, name='form_plays'),
    path('plays/get_play/<int:id>/add_repeat/', views.form_repeats, name='form_repeats'),

    path('plays/get_play/<int:id>', views.get_play, name='get_play'),
    path('plays/get_play/<int:id_play>/get_repeat/<int:id_repeat>', views.get_repeat, name='get_repeat'),

    path('employees/get_employee/<int:id>', views.get_employee, name='get_employee'),
    path('admin_section/', views.admin_section, name='admin_section'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-admin/', views.create_admin, name='create_admin'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
 
    path('employees/add_employee/', views.form_employees, name='form_employees'),

    path('ensembles/', views.list_ensembles, name='list_ensembles'),
    path('ensembles/add_ensemble/', views.form_ensembles, name='form_ensembles'),
    path('ensembles/get_ensemble/<int:id>', views.get_ensemble, name='get_ensemble'),
    path('ensembles/edit/<int:ensemble_id>/', views.edit_ensemble, name='edit_ensemble'),
    path('ensembles/copy/<int:ensemble_id>/', views.copy_ensemble, name='copy_ensemble'),

    path('plays/edit/<int:id>/', views.edit_play, name='edit_play'),
    path('plays/copy/<int:id>/', views.copy_play, name='copy_play'),

    path('plays/get_play/<int:id_play>/edit/<int:id_repeat>', views.edit_repeat, name='edit_repeat'),
    path('plays/get_play/<int:id_play>/copy/<int:id_repeat>', views.copy_repeat, name='copy_repeat'),
    path('employee/edit/<int:id>/', views.edit_employee, name='edit_employee'),

    path('concerts_and_events/add_concert_or_event/', views.form_concerts_and_events, name='form_concerts_and_events'),
    path('concerts_and_events/get_concert_or_event/<int:id_concert>', views.get_concert_or_event,
         name='get_concert_or_event'),
    path('concerts_and_events/edit/<int:concert_id>/', views.edit_concert, name='edit_concert'),
    path('concerts_and_events/copy/<int:concert_id>/', views.copy_concert, name='copy_concert'),

    path('autocomplete/', views.autocomplete, name='autocomplete')

]