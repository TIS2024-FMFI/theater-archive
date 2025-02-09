from django.contrib.auth.models import User
from django.db import models

class Ensemble(models.Model):
    name = models.CharField(max_length=100)
    guest = models.BooleanField(default=False) #vm44
    description = models.TextField(max_length=1500, null=True, blank=True) #vm44
    foundation_date = models.DateField() #co ak nebudu mat info, kedy vznikol subor? nebude lepsie dovolit aj tu null?
    dissolution_date = models.DateField(null=True, blank=True)
    publicity = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class GenreType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Play(models.Model):
    ensemble = models.ForeignKey('Ensemble', on_delete=models.CASCADE) # preco nie on_delete=models.SET_NULL ale on_delete=models.CASCADE? trochu nebezpecne
    genre_type = models.ForeignKey('GenreType', on_delete=models.SET_NULL, null=True, blank=True)
    author_first_name = models.CharField(max_length=100, null=True, blank=True)
    author_last_name = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank=True) #vm44
    description = models.TextField(max_length=1500, null=True, blank=True)
    publicity = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title


class Document(models.Model):
    document_path = models.CharField(max_length=100)

    def __str__(self):
        return self.document_path


class PlayDocument(models.Model):
    play = models.ForeignKey('Play', on_delete=models.CASCADE)
    document = models.ForeignKey('Document', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.play} - {self.document}"


class ConcertDocument(models.Model):
    concert = models.ForeignKey('Concert', on_delete=models.CASCADE)
    document = models.ForeignKey('Document', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.concert} - {self.document}"


class EmployeeDocument(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    document = models.ForeignKey('Document', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee} - {self.document}"


class EmployeeType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Employee(models.Model): # rename to Employees
    id = models.AutoField(primary_key=True)
    ensemble = models.ForeignKey('Ensemble', on_delete=models.SET_NULL, null=True)
    employee_type = models.ForeignKey('EmployeeType', on_delete=models.SET_NULL, null=True)
    genre_type = models.ForeignKey('GenreType', on_delete=models.SET_NULL, null=True) #vm44
    document = models.ForeignKey('Document', on_delete=models.SET_NULL, null=True, blank=True) #vm44 tabulka Document neexistuje

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_of_death = models.DateField(null=True) #vm44
    place_of_birth = models.CharField(max_length=100, null=True, blank=True)
    place_of_death = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=1500, null=True, blank=True) #vm44   
    publicity = models.BooleanField(default=False) #vm44

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class EmployeeJob(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee} - {self.job}"


class Job(models.Model):
    name = models.CharField(max_length=100)
    play_character = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PlayPerformer(models.Model):
    play = models.ForeignKey('Play', on_delete=models.CASCADE) # zase, preco CASCADE? Nie je to nebezpecne?
    employee = models.ForeignKey('Employee', null=True, on_delete=models.CASCADE) # nie je v modeli, naco sa to pridalo?
    employee_job = models.ForeignKey('EmployeeJob', on_delete=models.CASCADE)
    job = models.CharField(max_length=100) # nie je v modeli, naco sa to pridalo?

    def __str__(self):
        return f"{self.play} - {self.job}"


class Concert(models.Model):
    id = models.AutoField(primary_key=True) # redundant
    concert_type = models.ForeignKey('ConcertType', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1500, null=True, blank=True)
    

    def __str__(self):
        return self.name


class ConcertPerformer(models.Model):
    employee_job = models.ForeignKey('EmployeeJob', on_delete=models.CASCADE) #vm44
    #employee = models.ForeignKey('Employee', on_delete=models.CASCADE) # chyba? nie je v data modeli, alebo sa niekto rozhodol ze to je namiesto employee_job?
    concert = models.ForeignKey('Concert', on_delete=models.CASCADE)
    job = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.concert} - {self.job}"


class ConcertType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Repeat(models.Model):
    play = models.ForeignKey('Play', on_delete=models.CASCADE)
    repeat_type = models.ForeignKey('RepeatType', on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True)
    ensemble = models.ForeignKey('Ensemble', on_delete=models.SET_NULL, null=True) #vm44
    date = models.DateTimeField()
    publicity = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.play} - {self.date}"


class RepeatType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class RepeatPerformer(models.Model):
    repeat = models.ForeignKey('Repeat', on_delete=models.CASCADE)
    #employee_job = models.ForeignKey('EmployeeJob', on_delete=models.CASCADE) #vm44 chyba? alebo to je akoze rola?
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    role = models.CharField(max_length=100) #vm44

    def __str__(self):
        return f"{self.repeat} - {self.employee_job}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    real_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.real_name} ({self.user.username})"