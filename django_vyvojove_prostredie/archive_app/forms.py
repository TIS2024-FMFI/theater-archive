from django import forms
from .models import *

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'ensemble', 'employee_type', 'genre_type',
            'first_name', 'last_name', 'date_of_birth', 'date_of_death',
            'place_of_birth', 'place_of_death', 'description', 'publicity'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_death': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class EmployeeJobForm(forms.ModelForm):
    class Meta:
        model = EmployeeJob
        fields = ['job', 'date_start', 'date_end']
        widgets = {
            'date_start': forms.DateInput(attrs={'type': 'date'}),
            'date_end': forms.DateInput(attrs={'type': 'date'}),
        }


class PlayForm(forms.ModelForm):
    class Meta:
        model = Play
        fields = [
            'title', 'author_first_name', 'author_last_name', 'description', 'publicity', 'ensemble', 'genre_type'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }