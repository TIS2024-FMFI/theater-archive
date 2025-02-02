from django import forms
from .models import Employee, EmployeeJob

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'publicity']
        widgets = {
            'publicity': forms.CheckboxInput(),
        }

class EmployeeJobForm(forms.ModelForm):
    class Meta:
        model = EmployeeJob
        fields = ['job', 'date_start', 'date_end']
        widgets = {
            'date_start': forms.DateInput(attrs={'type': 'date'}),
            'date_end': forms.DateInput(attrs={'type': 'date'}),
        }
