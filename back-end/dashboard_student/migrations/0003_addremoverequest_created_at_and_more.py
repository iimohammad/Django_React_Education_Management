# Generated by Django 4.2 on 2024-03-28 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_teacher_can_be_advisor'),
        ('dashboard_student', '0002_remove_semesterregistrationrequest_requested_courses_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='addremoverequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-03-28 10:10:10'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addremoverequest',
            name='educational_assistant_visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='addremoverequest',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='addremoverequest',
            name='student',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='accounts.student'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addremoverequest',
            name='teacher_visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='emergencyremovalrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-03-28 10:10:10'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emergencyremovalrequest',
            name='educational_assistant_visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='emergencyremovalrequest',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='emergencyremovalrequest',
            name='student',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='accounts.student'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emergencyremovalrequest',
            name='teacher_visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employmenteducationrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-03-28 10:10:10'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employmenteducationrequest',
            name='educational_assistant_visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employmenteducationrequest',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employmenteducationrequest',
            name='student',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='accounts.student'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employmenteducationrequest',
            name='teacher_visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='enrollmentrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-03-28 10:10:10'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='enrollmentrequest',
            name='educational_assistant_visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='enrollmentrequest',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='enrollmentrequest',
            name='student',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='accounts.student'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='enrollmentrequest',
            name='teacher_visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='revisionrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-03-28 10:10:10'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='revisionrequest',
            name='educational_assistant_visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='revisionrequest',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='revisionrequest',
            name='student',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='accounts.student'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='revisionrequest',
            name='teacher_visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='semesterregistrationrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-03-28 10:10:10'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='semesterregistrationrequest',
            name='educational_assistant_visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='semesterregistrationrequest',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='semesterregistrationrequest',
            name='student',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='accounts.student'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='semesterregistrationrequest',
            name='teacher_visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentdeletesemesterrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-03-28 10:10:10'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdeletesemesterrequest',
            name='educational_assistant_visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentdeletesemesterrequest',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentdeletesemesterrequest',
            name='student',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='accounts.student'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdeletesemesterrequest',
            name='teacher_visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='unitselectionrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-03-28 10:10:10'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unitselectionrequest',
            name='educational_assistant_visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='unitselectionrequest',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='unitselectionrequest',
            name='student',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='accounts.student'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unitselectionrequest',
            name='teacher_visited',
            field=models.BooleanField(default=False),
        ),
    ]
