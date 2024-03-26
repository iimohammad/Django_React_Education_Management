# Generated by Django 4.2 on 2024-03-25 21:09

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
                ('corequisite', models.ManyToManyField(related_name='corequisites', to='education.course')),
                ('prerequisite', models.ManyToManyField(related_name='prerequisites', to='education.course')),
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
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_semester', models.DateTimeField()),
                ('end_semester', models.DateTimeField()),
                ('semester_type', models.CharField(choices=[('F', 'Fall'), ('W', 'Winter'), ('S', 'Summer')], default='F', max_length=1)),
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
                ('course_capacity', models.PositiveIntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.course')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.teacher')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.semester')),
            ],
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('R', 'Registered'), ('P', 'Pending'), ('W', 'Withdrawn')], default='R', max_length=1)),
                ('score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='education.semestercourse')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='SemesterUnitSelection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_selection_start', models.DateField()),
                ('unit_selection_end', models.DateField()),
                ('semester', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='education.semester')),
            ],
        ),
        migrations.CreateModel(
            name='SemesterExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_start', models.DateField()),
                ('exam_end', models.DateField()),
                ('semester', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='education.semester')),
            ],
        ),
        migrations.CreateModel(
            name='SemesterEmergency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emergency_remove_start', models.DateField()),
                ('emergency_remove_end', models.DateField()),
                ('semester', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='education.semester')),
            ],
        ),
        migrations.CreateModel(
            name='SemesterClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classes_start', models.DateField()),
                ('classes_end', models.DateField()),
                ('semester', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='education.semester')),
            ],
        ),
        migrations.CreateModel(
            name='SemesterAddRemove',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addremove_start', models.DateField()),
                ('addremove_end', models.DateField()),
                ('semester', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='education.semester')),
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
    ]
