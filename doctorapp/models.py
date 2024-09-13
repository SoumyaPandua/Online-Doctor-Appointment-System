from django.db import models
from authapp.models import *

class DoctorTimetable(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    SHIFT_CHOICES = [
        ('shift1', 'Shift 1'),
        ('shift2', 'Shift 2'),
    ]

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='timetable')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    avg_consult_time = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.doctor} - {self.day} {self.shift}"

    class Meta:
        unique_together = ('doctor', 'day', 'shift')  # Prevent duplicate day/shift for the same doctor



class Appointment(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    CONSULTATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    apt_no = models.CharField(max_length=20,primary_key=True)
    apt_date = models.DateField()
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=255)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=20)
    patient_age = models.PositiveIntegerField()
    patient_dob = models.DateField()
    patient_gender = models.CharField(max_length=10)
    patient_comment = models.TextField(blank=True, null=True)
    doctor_comment = models.TextField(blank=True, null=True)
    consultation_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    consultation_status = models.CharField(max_length=20, choices=CONSULTATION_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Appointment {self.apt_no} - {self.patient_name} with {self.doctor.get_full_name()}"
