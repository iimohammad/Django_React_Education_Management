# Generated by Django 4.2 on 2024-03-26 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0006_course_department'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentcourse',
            old_name='course',
            new_name='semester_course',
        ),
    ]
