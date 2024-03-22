# Generated by Django 4.2 on 2024-03-21 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=40)),
                ('course_code', models.PositiveSmallIntegerField()),
                ('credit_num', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=40)),
                ('department_code', models.PositiveSmallIntegerField()),
                ('year_established', models.DateField()),
                ('department_location', models.TextField(blank=True)),
                ('number_of_students', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('selection_start', models.DateTimeField()),
                ('selection_end', models.DateTimeField()),
                ('start_semester', models.DateTimeField()),
                ('end_semester', models.DateTimeField()),
                ('exam_start', models.DateTimeField()),
                ('exam_end', models.DateTimeField()),
                ('add_remove_start', models.DateTimeField()),
                ('add_remove_end', models.DateTimeField()),
                ('emergency_remove_start', models.DateTimeField()),
                ('emergency_remove_end', models.DateTimeField()),
                ('classes_start', models.DateTimeField()),
                ('classes_end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('R', 'Registered'), ('P', 'Pending'), ('W', 'Withdrawn')], default='R', max_length=1)),
                ('score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='SemesterCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_days', models.CharField(blank=True, choices=[('saturday', 'Saturday'), ('sunday', 'Sunday'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday')], max_length=20, null=True)),
                ('class_time', models.TimeField()),
                ('exam_datetime', models.DateTimeField()),
                ('exam_location', models.CharField(max_length=100)),
                ('class_capacity', models.PositiveIntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.course')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.teacher')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.semester')),
            ],
        ),
        migrations.CreateModel(
            name='Prerequisite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prerequisites', to='education.course')),
                ('prerequisite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='required_by', to='education.course')),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major_name', models.CharField(max_length=30)),
                ('major_code', models.PositiveSmallIntegerField()),
                ('number_of_credits', models.PositiveIntegerField()),
                ('level', models.CharField(choices=[('B', 'Bachelor'), ('M', 'Master'), ('P', 'PhD')], default='B', max_length=1)),
                ('education_group', models.CharField(max_length=30)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.department')),
            ],
        ),
        migrations.CreateModel(
            name='Corequisite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corequisite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='required_with', to='education.course')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='corequisites', to='education.course')),
            ],
        ),
    ]
