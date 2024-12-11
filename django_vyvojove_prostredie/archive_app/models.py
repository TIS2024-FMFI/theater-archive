from django.db import models

class Ensemble(models.Model):
    name = models.CharField(max_length=100)
    foundation_date = models.DateField()
    dissolution_date = models.DateField(null=True, blank=True)
    
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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    ensemble = models.ForeignKey('Ensemble', on_delete=models.SET_NULL, null=True)
    employee_type = models.ForeignKey('EmployeeType', on_delete=models.SET_NULL, null=True)

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

    def __str__(self):
        return self.name


class PlayPerformer(models.Model):
    play = models.ForeignKey('Play', on_delete=models.CASCADE)
    employee_job = models.ForeignKey('EmployeeJob', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.play} - {self.employee_job}"


class Concert(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    concert_type = models.ForeignKey('ConcertType', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class ConcertPerformer(models.Model):
    concert = models.ForeignKey('Concert', on_delete=models.CASCADE)
    employee_job = models.ForeignKey('EmployeeJob', on_delete=models.CASCADE)
    job = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.concert} - {self.employee_job} ({self.job})"


class ConcertType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Repeat(models.Model):
    play = models.ForeignKey('Play', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()
    publicity = models.BooleanField(default=False)
    repeat_type = models.ForeignKey('RepeatType', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.play} - {self.date}"


class RepeatType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class RepeatPerformer(models.Model):
    repeat = models.ForeignKey('Repeat', on_delete=models.CASCADE)
    employee_job = models.ForeignKey('EmployeeJob', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.repeat} - {self.employee_job}"
