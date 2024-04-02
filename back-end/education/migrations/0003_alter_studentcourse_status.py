# Generated by Django 4.2 on 2024-04-01 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_alter_studentcourse_semester_course_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentcourse',
            name='status',
            field=models.CharField(choices=[('F', 'FinalRegistered'), ('R', 'Registered'), ('P', 'Pending'), ('W', 'Withdrawn'), ('D', 'Deleted')], default='R', max_length=1),
        ),
    ]
