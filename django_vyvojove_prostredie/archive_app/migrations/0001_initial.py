# Generated by Django 5.1.3 on 2024-12-04 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ensemble',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('foundation_date', models.DateField()),
                ('dissolution_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GenreType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('place_of_birth', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('employee_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='archive_app.employeetype')),
                ('ensemble', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='archive_app.ensemble')),
            ],
        ),
        migrations.CreateModel(
            name='Play',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author_first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('author_last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('publicity', models.BooleanField(default=False)),
                ('ensemble', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive_app.ensemble')),
                ('genre_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='archive_app.genretype')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job', models.CharField(max_length=50)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='archive_app.employee')),
                ('play', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='archive_app.play')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_path', models.CharField(max_length=100)),
                ('play', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='archive_app.play')),
            ],
        ),
        migrations.CreateModel(
            name='Repeat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('publicity', models.BooleanField(default=False)),
                ('play', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repeats', to='archive_app.play')),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='archive_app.room')),
            ],
        ),
    ]
