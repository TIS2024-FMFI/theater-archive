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
        fields = "__all__"
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_death': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['date_of_death'].required = False
        self.fields['place_of_death'].required = False


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

    def __init__(self, *args, **kwargs):
        super(EmployeeJobForm, self).__init__(*args, **kwargs)
        self.fields['date_end'].required = False


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


class EnsembleForm(forms.ModelForm): #vm44
    class Meta:
        model = Ensemble
        fields = ['name', 'guest', 'foundation_date', 'dissolution_date', 'description', 'publicity']
        widgets = {
            'foundation_date': forms.DateInput(attrs={'type': 'date'}),
            'dissolution_date': forms.DateInput(attrs={'type': 'date'}),
        }


class RepeatForm(forms.ModelForm):
    class Meta:
        model = Repeat
        fields = '__all__'
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'publicity': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Checkbox styling
            'play': forms.Select(attrs={'class': 'form-select'}),  # Dropdown styling
            'room': forms.Select(attrs={'class': 'form-select'}),
            'repeat_type': forms.Select(attrs={'class': 'form-select'}),
            'ensemble': forms.Select(attrs={'class': 'form-select'}),
        }


class RepeatPerformerForm(forms.ModelForm):
    class Meta:
        model = RepeatPerformer
        fields = ['repeat', 'employee_job']
        widgets = {
            'repeat': forms.Select(attrs={'class': 'form-select'}),  # Dropdown styling
            'employee_job': forms.Select(attrs={'class': 'form-select'}),
        }