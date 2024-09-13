from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

class WebsiteContent(models.Model):
    title = models.CharField(max_length=100, default="Doctor Appointment System")
    favicon = models.ImageField(upload_to='images/', default='images/favicon.ico')
    logo_image = models.ImageField(upload_to='images/', default='images/manas.jpg')
    home_image = models.ImageField(upload_to='images/', default='images/doctor.jpg')
    about_image = models.ImageField(upload_to='images/', default='images/about.jpg')
    teeth_image = models.ImageField(upload_to='images/', default='images/teeth.jpeg')
    faq_image = models.ImageField(upload_to='images/', default='images/faq.png')
    address_line1 = models.CharField(max_length=255, default="S.G Palya, Koramangala")
    address_line2 = models.CharField(max_length=255, default="Bangalore, Karnataka")
    phone_number = models.CharField(max_length=20, default="+91 9234123456")
    email = models.EmailField(default="axyz10649@gmail.com")
    copyright_text = models.CharField(max_length=255, default="copyrigt@Soumyaranjan Pandua")
    about_text = models.TextField(default="We are dedicated to providing the best healthcare services to our patients. Our team of experienced doctors is here to ensure your well-being and health.")
    domain = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question


class Department(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('department_detail', args=[str(self.id)])
    

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=20, help_text="Maximum 20 words.")
    rating = models.IntegerField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.rating} stars"
