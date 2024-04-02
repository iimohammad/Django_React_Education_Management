# Generated by Django 4.2 on 2024-04-02 15:25

import accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_adminuser_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='national_code',
            field=models.CharField(blank=True, max_length=10, validators=[accounts.validators.validate_national_code]),
        ),
    ]
