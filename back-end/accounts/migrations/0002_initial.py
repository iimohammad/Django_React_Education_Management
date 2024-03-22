# Generated by Django 4.2 on 2024-03-22 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('education', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='education.department'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='past_courses',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='education.course'),
        ),
        migrations.AddField(
            model_name='student',
            name='advisor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.teacher'),
        ),
        migrations.AddField(
            model_name='student',
            name='entry_semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='education.semester'),
        ),
        migrations.AddField(
            model_name='student',
            name='major',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='education.major'),
        ),
        migrations.AddField(
            model_name='educationalassistant',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='education.department'),
        ),
        migrations.AddField(
            model_name='educationalassistant',
            name='field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='education.major'),
        ),
    ]
