from django.contrib.auth.models import User
from django.db import models

class Ensemble(models.Model):
    name = models.CharField(max_length=100)
    foundation_date = models.DateField(null=True)
    dissolution_date = models.DateField(null=True, blank=True)
    guest = models.BooleanField(default=False) #vm44
    description = models.TextField(max_length=1500, null=True, blank=True) #vm44
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
    title = models.CharField(max_length=200)
    author_first_name = models.CharField(max_length=100, null=True, blank=True)
    author_last_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    publicity = models.BooleanField(default=False)
    ensemble = models.ForeignKey('Ensemble', on_delete=models.CASCADE)
    genre_type = models.ForeignKey('GenreType', on_delete=models.SET_NULL, null=True, blank=True)
    subtitle = models.CharField(max_length=200, null=True, blank=True) #vm44

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


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    ensemble = models.ForeignKey('Ensemble', on_delete=models.SET_NULL, null=True)
    employee_type = models.ForeignKey('EmployeeType', on_delete=models.SET_NULL, null=True)
    genre_type = models.ForeignKey('GenreType', on_delete=models.SET_NULL, null=True) #vm44
    #document = models.ForeignKey('EmployeeDocument', on_delete=models.SET_NULL, null=True, blank=True) #nepotrebujeme

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_of_death = models.DateField(null=True) #vm44
    place_of_birth = models.CharField(max_length=100, null=True, blank=True)
    place_of_death = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)    
    publicity = models.BooleanField(default=False) #vm44
    date_publicity = models.BooleanField(default=False) #vm44

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
    name = models.CharField(max_length=50)
    play_character = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PlayPerformer(models.Model):
    play = models.ForeignKey('Play', on_delete=models.CASCADE)
    employee = models.ForeignKey('Employee', null=True, on_delete=models.CASCADE)
    employee_job = models.ForeignKey('EmployeeJob', on_delete=models.CASCADE)
    job = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.play} - {self.job}"


class Concert(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    concert_type = models.ForeignKey('ConcertType', on_delete=models.SET_NULL, null=True)
    publicity = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ConcertPerformer(models.Model):
    concert = models.ForeignKey('Concert', on_delete=models.CASCADE)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    job = models.CharField(max_length=50) 

    def __str__(self):
        return f"{self.concert} - {self.job}"


class ConcertType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Repeat(models.Model):
    play = models.ForeignKey('Play', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField( )
    publicity = models.BooleanField(default=False)
    repeat_type = models.ForeignKey('RepeatType', on_delete=models.SET_NULL, null=True)
    ensemble = models.ForeignKey('Ensemble', on_delete=models.SET_NULL, null=True) #vm44

    def __str__(self):
        return f"{self.play} - {self.date}"


class RepeatType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class RepeatPerformer(models.Model):
    repeat = models.ForeignKey('Repeat', on_delete=models.CASCADE)
    employee_job = models.ForeignKey('EmployeeJob', on_delete=models.CASCADE) #toto je rola

    def __str__(self):
        return f"{self.repeat} - {self.employee_job}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    real_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.real_name} ({self.user.username})"