# Generated by Django 4.2 on 2024-04-02 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_course_availablity_course_course_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]