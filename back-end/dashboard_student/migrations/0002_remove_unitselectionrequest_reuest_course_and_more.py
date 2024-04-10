# Generated by Django 4.2 on 2024-04-10 03:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_alter_course_course_code_and_more'),
        ('accounts', '0004_remove_student_gpa'),
        ('dashboard_student', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unitselectionrequest',
            name='reuest_course',
        ),
        migrations.AddField(
            model_name='unitselectionrequest',
            name='request_course',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='education.semestercourse'),
        ),
        migrations.AddField(
            model_name='unitselectionrequest',
            name='student',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='accounts.student'),
        ),
        migrations.AlterField(
            model_name='unitselectionrequest',
            name='approval_status',
            field=models.CharField(choices=[('R', 'Registered'), ('R', 'Reserved')], max_length=1),
        ),
    ]
