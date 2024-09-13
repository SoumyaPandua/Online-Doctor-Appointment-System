# Generated by Django 5.0.4 on 2024-08-26 13:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authapp', '0002_adminprofile_is_admin_doctorprofile_is_doctor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorTimetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')], max_length=10)),
                ('shift', models.CharField(choices=[('shift1', 'Shift 1'), ('shift2', 'Shift 2')], max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('avg_consult_time', models.IntegerField(default=10)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetable', to='authapp.doctorprofile')),
            ],
            options={
                'unique_together': {('doctor', 'day', 'shift')},
            },
        ),
    ]
