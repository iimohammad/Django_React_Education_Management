# Generated by Django 4.2 on 2024-04-01 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_adminuser_user'),
        ('education', '0003_alter_studentcourse_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='availablity',
            field=models.CharField(choices=[('A', 'Available'), ('D', 'Deleted')], default='A', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='course_type',
            field=models.CharField(choices=[('L', 'Laboratory'), ('R', 'Research'), ('I', 'Internship'), ('A', 'Activity '), ('G', 'General'), ('B', 'Basic')], default='B', max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='major',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='education.major'),
        ),
        migrations.AlterField(
            model_name='major',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='education.department'),
        ),
        migrations.AlterField(
            model_name='semestercourse',
            name='exam_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='semestercourse',
            name='exam_location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='studentcourse',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.student'),
        ),
    ]
