# Generated by Django 5.1.5 on 2025-02-12 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='file',
            new_name='document_path',
        ),
    ]
