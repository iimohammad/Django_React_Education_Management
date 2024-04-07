# Generated by Django 4.2 on 2024-04-06 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('education', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SemesterRegistrationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('requested_courses', models.ManyToManyField(blank=True, to='education.semestercourse', verbose_name='Requested_courses')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='education.semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='UnitSelectionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('requested_courses', models.ManyToManyField(blank=True, to='education.semestercourse', verbose_name='Requested_courses')),
                ('semester_registration_request', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='dashboard_student.semesterregistrationrequest')),
            ],
        ),
        migrations.CreateModel(
            name='StudentDeleteSemesterRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_approval_status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=1)),
                ('educational_assistant_approval_status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student_explanations', models.TextField()),
                ('educational_assistant_explanation', models.TextField()),
                ('semester_registration_request', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard_student.semesterregistrationrequest')),
            ],
        ),
        migrations.CreateModel(
            name='RevisionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_approval_status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=1)),
                ('educational_assistant_approval_status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
                ('answer', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='education.studentcourse')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='EnrollmentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reason_text', models.TextField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='EmploymentEducationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('need_for', models.TextField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='EmergencyRemovalRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student_explanation', models.TextField()),
                ('educational_assistant_explanation', models.TextField()),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='education.studentcourse')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='AddRemoveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('added_courses', models.ManyToManyField(related_name='added_courses', to='education.semestercourse')),
                ('removed_courses', models.ManyToManyField(related_name='removed_courses', to='education.studentcourse')),
                ('semester_registration_request', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard_student.semesterregistrationrequest')),
            ],
        ),
    ]
