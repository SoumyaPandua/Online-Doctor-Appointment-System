# Generated by Django 5.0.4 on 2024-09-01 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_remove_doctorprofile_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorprofile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
