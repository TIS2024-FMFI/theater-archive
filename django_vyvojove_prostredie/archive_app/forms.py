from django import forms
from django.forms import inlineformset_factory
from .models import *

class EmployeeForm(forms.ModelForm):
    ensemble = forms.ModelChoiceField(
        queryset=Ensemble.objects.all(),
        empty_label="Select Ensemble",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    employee_type = forms.ModelChoiceField(
        queryset=EmployeeType.objects.all(),
        empty_label="Select Employee Type",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    genre_type = forms.ModelChoiceField(
        queryset=GenreType.objects.all(),
        empty_label="Select Genre Type",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Employee
        fields = [
            'ensemble', 'employee_type', 'genre_type', 'first_name', 'last_name',
            'date_of_birth', 'date_of_death', 'place_of_birth', 'place_of_death',
            'description', 'publicity'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_death': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class EmployeeJobForm(forms.ModelForm):
    job = forms.ModelChoiceField(
        queryset=Job.objects.filter(play_character=False),
        required=False,  # Allow empty so users can enter a new job
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Existing Job"
    )

    new_job_name = forms.CharField(
        max_length=100,
        required=False,  # Optional: only used if user wants to add a new job
        widget=forms.TextInput(attrs={'placeholder': 'Or enter a new job'}),
        label="Or Add New Job"
    )

    class Meta:
        model = EmployeeJob
        fields = ['job', 'new_job_name', 'date_start', 'date_end']
        widgets = {
            'date_start': forms.DateInput(attrs={'type': 'date'}),
            'date_end': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        job = cleaned_data.get("job")
        new_job_name = cleaned_data.get("new_job_name")

        if not job and not new_job_name:
            raise forms.ValidationError("Please select an existing job or enter a new one.")

        if new_job_name:
            job, created = Job.objects.get_or_create(name=new_job_name)
            cleaned_data["job"] = job  # Use the newly created job

        return cleaned_data


class PlayForm(forms.ModelForm):
    genre_type = forms.ModelChoiceField(
        queryset=GenreType.objects.all(),
        empty_label="Select Genre",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    ensemble = forms.ModelChoiceField(
        queryset=Ensemble.objects.all(),
        empty_label="Select Ensemble",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Play
        fields = ['title', 'author_first_name', 'author_last_name', 'genre_type', 'ensemble', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


EmployeeJobFormSet = inlineformset_factory(
    Employee, EmployeeJob,
    form=EmployeeJobForm,
    extra=1,
    # can_delete=True
)
