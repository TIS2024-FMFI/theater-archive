from django import forms
from django.forms import inlineformset_factory
from .models import *
from django.utils import timezone
from django.db import IntegrityError

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

        # if not job and not new_job_name:
        #     raise forms.ValidationError("Prosísm vyberte zamestnanie alebo zadajte nové.")

        if new_job_name:
            job, created = Job.objects.get_or_create(name=new_job_name)
            cleaned_data["job"] = job  # Use the newly created job

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(EmployeeJobForm, self).__init__(*args, **kwargs)
        self.fields['date_end'].required = False
        self.fields['date_start'].required = False


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
        fields = "__all__"
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
    repeat_type = forms.ModelChoiceField(
        queryset=RepeatType.objects.all(),
        empty_label="Typ reprízy",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        empty_label="Miestnosť",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    new_room = forms.CharField(
        required=False,  # Allow entering a custom room
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Iná miestnosť'})
    )

    ensemble = forms.ModelChoiceField(
        queryset=Ensemble.objects.all(),
        empty_label="Select Ensemble",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Repeat
        exclude = ['play']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'publicity': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Checkbox styling
        }

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get("room")
        new_room = cleaned_data.get("new_room")

        if not room and not new_room:
            raise forms.ValidationError("Prosím vybertie miesto alebo zadajte nové.")

        if new_room:
            room, created = Room.objects.get_or_create(name=new_room)
            cleaned_data["room"] = room  # Use the newly created room
        return cleaned_data


class RepeatPerformerForm(forms.ModelForm):
    employee = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Umelec'})
    )

    job_name = forms.CharField(
        required=False,  # Allow entering a custom job
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postava'})
    )

    class Meta:
        model = RepeatPerformer
        fields = ['repeat', 'employee', 'job_name']

    def save(self, commit=True):
        repeat_performer = super().save(commit=False)
        employee_name  = self.cleaned_data['employee'].strip()
        job_name = self.cleaned_data.get('job_name', '').strip()

        name_parts = employee_name.split()
        if employee_name == "":
            repeat_performer.employee_job = None
            return repeat_performer

        if len(name_parts) < 2:
            raise forms.ValidationError("Zadajte korektné meno všetkých umelcov.")

        first_name, last_name = name_parts[0], " ".join(name_parts[1:])
        try:
            employee = Employee.objects.get(first_name=first_name, last_name=last_name)
        except Employee.DoesNotExist:
            raise forms.ValidationError("Umelec neexistuje. Zadajte korektné meno všetkých umelcov.")


        job, created = Job.objects.get_or_create(name=job_name) if job_name else (None, False)
        if job:
            job.play_character = True
            job.save()
            try:
                print("Employee, job:", employee, job)
                employee_job = EmployeeJob.objects.get(employee=employee, job=job)
                print("     ", employee_job)
            except EmployeeJob.DoesNotExist:
                employee_job, created = EmployeeJob.objects.get_or_create(
                    employee=employee,
                    job=job,  # Assign the newly created or existing job
                    date_start=timezone.now()
                )

            repeat_performer.employee_job = employee_job  # Assign EmployeeJob to RepeatPerformer

        if commit:
            repeat_performer.save()

        return repeat_performer

class ConcertForm(forms.ModelForm):
    concert_type = forms.ModelChoiceField(
        queryset=ConcertType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Concert
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Názov koncertu / podujatia'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Sem píšte popis...'}),
        }


class ConcertPerformerForm(forms.ModelForm): #ucinkujuci
    employee_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Umelec',
            'data-url': "autocomplete/"
        })
    )

    job = forms.CharField(
        required=False,  # Allow entering a custom job
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pozícia účinkujúceho'})
    )

    class Meta:
        model = ConcertPerformer
        fields = ['employee_name', 'job']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.employee:
                self.fields[
                    'employee_name'].initial = f"{self.instance.employee.first_name} {self.instance.employee.last_name}"


    def save(self, commit=True):
        concert_performer = super().save(commit=False)
        employee_name  = self.cleaned_data['employee_name'].strip()
        job = self.cleaned_data.get('job', '').strip()

        name_parts = employee_name.split()
        if len(name_parts) < 2:
            raise forms.ValidationError("Zadajte korektné meno všetkých účinkujúcich.")

        first_name, last_name = name_parts[0], " ".join(name_parts[1:])
        print(first_name, last_name)
        try:
            employee = Employee.objects.get(first_name=first_name, last_name=last_name)
            print("Employee, job:", employee, job)
        except Employee.DoesNotExist:
            raise forms.ValidationError("Účinkujúci neexistuje. Zadajte korektné meno všetkých účinkujúcich.")


        concert_performer.employee = employee
        concert_performer.job = job
        if commit:
            concert_performer.save()

        return concert_performer


class DocumentForm(forms.ModelForm):
    document_path = forms.FileField(required=False)

    class Meta:
        model = Document
        fields = ['document_path']



class PlayPerformerForm(forms.ModelForm):
    employee_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Umelec'})
    )

    job_name = forms.CharField(
        required=False,  # Allow entering a custom job
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Úloha'})
    )

    class Meta:
        model = PlayPerformer
        fields = ['play', 'employee_name', 'job_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.employee:
                self.fields[
                    'employee_name'].initial = f"{self.instance.employee.first_name} {self.instance.employee.last_name}"

    def save(self, commit=True):
        play_performer = super().save(commit=False)
        employee_name  = self.cleaned_data['employee_name'].strip()
        job_name = self.cleaned_data.get('job_name', '').strip()

        name_parts = employee_name.split()
        if employee_name == "":
            return play_performer

        if len(name_parts) < 2:
            raise forms.ValidationError("Zadajte korektné meno všetkých umelcov.")

        first_name, last_name = name_parts[0], " ".join(name_parts[1:])
        try:
            employee = Employee.objects.get(first_name=first_name, last_name=last_name)
        except Employee.DoesNotExist:
            raise forms.ValidationError("Umelec neexistuje. Zadajte korektné meno všetkých umelcov.")


        job, created = Job.objects.get_or_create(name=job_name) if job_name else (None, False)
        if job:
            job.play_character = False
            job.save()
            try:
                print("Employee, job:", employee, job)
                employee_job = EmployeeJob.objects.get(employee=employee, job=job)
                print("     ", employee_job)
            except EmployeeJob.DoesNotExist:
                employee_job, created = EmployeeJob.objects.get_or_create(
                    employee=employee,
                    job=job,  # Assign the newly created or existing job
                    date_start=timezone.now()
                )

            play_performer.employee_job = employee_job  # Assign EmployeeJob to RepeatPerformer

        if commit:
            play_performer.save()

        return play_performer


PlayPerformerFormSet = inlineformset_factory(
    Play, PlayPerformer,
    form=PlayPerformerForm,
    extra=1,  # Allow adding at least one performer
    can_delete=True  # Allow deleting performers
)

RepeatPerformerFormSet = inlineformset_factory(
    Repeat, RepeatPerformer,
    form=RepeatPerformerForm,
    extra=1,
    can_delete=True
)

ConcertPerformerFormSet = inlineformset_factory(
    Concert, ConcertPerformer,
    form=ConcertPerformerForm,
    extra=1,
    can_delete=True
)

EmployeeJobFormSet = inlineformset_factory(
    Employee, EmployeeJob,
    form=EmployeeJobForm,
    extra=1,
    can_delete=True
)