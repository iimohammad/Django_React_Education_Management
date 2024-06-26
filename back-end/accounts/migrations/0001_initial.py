# Generated by Django 4.2 on 2024-04-12 19:16

import accounts.validators
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_number', models.CharField(blank=True, max_length=255)),
                ('national_code', models.CharField(blank=True, max_length=10, validators=[accounts.validators.validate_national_code])),
                ('birthday', models.DateField(blank=True, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='accounts/profile_images/')),
                ('phone', models.CharField(blank=True, max_length=15, validators=[accounts.validators.PhoneValidator()])),
                ('address', models.TextField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('MF', 'Unset')], default='MF', max_length=2)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='EducationalAssistant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_semester', models.CharField(max_length=100)),
                ('entry_year', models.CharField(max_length=4)),
                ('military_service_status', models.CharField(choices=[('EP', 'Education Pardon'), ('P', 'Passed'), ('E', 'Exempted'), ('F', 'Finished')], default='EP', max_length=2)),
                ('year_of_study', models.PositiveSmallIntegerField()),
                ('gpa_student', models.PositiveBigIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expertise', models.CharField(max_length=255)),
                ('rank', models.CharField(choices=[('I', 'Instructor'), ('ASP', 'Assistant Professor'), ('ACP', 'Associate Professor'), ('P', 'Professor')], default='I', max_length=3)),
                ('can_be_advisor', models.BooleanField(default=False)),
            ],
        ),
    ]
