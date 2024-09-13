from django.db import models
from django.contrib.auth.models import User
from website.models import Department
from datetime import date
from django.utils.translation import gettext_lazy as _

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    profile_image = models.ImageField(upload_to='images/', blank=True, null=True)
    address = models.TextField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.user.is_active = True
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    designation = models.CharField(max_length=100, blank=True, null=True)
    qualification = models.CharField(max_length=100, blank=True, null=True)
    experience = models.PositiveIntegerField(default=0)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    consultant_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profile_image = models.ImageField(upload_to='images/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    is_doctor = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.user.is_active = True
        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.save()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"
    
    def get_timetable(self):
        return self.timetable.all()
    
    def get_profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        return 'path/to/default/image.jpg'

    def __str__(self):
        return self.get_full_name()
    

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    dob = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='images/', blank=True, null=True)
    address = models.TextField(max_length=255, blank=True, null=True)
    is_patient = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.user.is_active = True
        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.save()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def get_profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        return 'path/to/default/image.jpg'

    @property
    def age(self):
        if self.dob:
            today = date.today()
            age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
            return age
        return _('Unknown')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
