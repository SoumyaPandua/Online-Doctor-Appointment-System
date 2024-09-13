from django.shortcuts import render, get_object_or_404, redirect
from collections import defaultdict
from .models import *
from authapp.models import *
from doctorapp.models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta,datetime
from django.http import JsonResponse
import random
import string
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def website_view(request):
    content = WebsiteContent.objects.first()
    faqs = FAQ.objects.all()
    departments = Department.objects.all()
    ratings = Rating.objects.all()
    return render(request, 'website.html', {'content': content, 'faqs': faqs, 'departments': departments, 'ratings': ratings})


def department_detail_view(request, department_name):
    content = WebsiteContent.objects.first()
    department = get_object_or_404(Department, name__iexact=department_name)
    doctors = DoctorProfile.objects.filter(department=department)
    return render(request, f"{department_name.lower()}_department.html", {
        'content': content,
        'department': department,
        'doctors': doctors,
    })

@login_required
def readmore_doctor_view(request, doctor_id):
    content = WebsiteContent.objects.first()
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    timetable_entries = doctor.get_timetable()
    timetable = defaultdict(list)
    for entry in timetable_entries:
        timetable[entry.day].append(entry)
    return render(request, 'readmore_doctor.html', {
        'content': content,
        'doctor': doctor,
        'timetable': dict(timetable),
    })


def generate_appointment_number_view(length=8):
    """Generate a random appointment number with a mix of letters and digits."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def calculate_age_view(dob):
    today = timezone.now().date()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

@login_required
def doctor_booking_view(request, doctor_id):
    content = WebsiteContent.objects.first()
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    patient = get_object_or_404(PatientProfile, user=request.user)

    today = datetime.now().date()
    available_dates = [today + timedelta(days=i) for i in range(1, 4)]
    patient_age = calculate_age_view(patient.dob) if patient.dob else None

    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            selected_date = request.POST.get('date')
            if selected_date:
                selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
                day_name = selected_date_obj.strftime('%A').lower()

                shifts = DoctorTimetable.objects.filter(doctor=doctor, day=day_name).values_list('shift', flat=True)
                if not shifts:
                    return JsonResponse({'message': 'No shifts set by doctor'})
                return JsonResponse({'shifts': list(shifts)})

        else:  # Handle normal form submission
            selected_date = request.POST.get('date')
            selected_shift = request.POST.get('shift')

            if selected_date and selected_shift:
                appointment_number = generate_appointment_number_view()

                Appointment.objects.create(
                    apt_no=appointment_number,
                    apt_date=datetime.strptime(selected_date, '%Y-%m-%d').date(),
                    doctor=doctor,
                    patient=patient,
                    patient_name=patient.user.get_full_name(),
                    patient_email=patient.user.email,
                    patient_phone=patient.phone,
                    patient_age=patient_age,
                    patient_dob=patient.dob,
                    patient_gender=patient.gender,
                    status='booked',
                    consultation_status='pending',
                    doctor_comment=request.POST.get('doctor-comment', ''),
                    patient_comment=request.POST.get('comment', ''),
                )
                return redirect('rating')

    context = {
        'content': content,
        'doctor': doctor,
        'patient': patient,
        'available_dates': available_dates,
        'patient_age': patient_age,
    }
    return render(request, 'doctor_booking.html', context)

@login_required
def rating_view(request):
    content = WebsiteContent.objects.first()
    patient = PatientProfile.objects.get(user=request.user)

    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating_value = request.POST.get('rating')
        image = patient.profile_image

        if comment and rating_value:
            Rating.objects.create(
                user=request.user,
                image=image,
                comment=comment,
                rating=rating_value,
            )
            return redirect('/')

    context = {
        'content': content,
        'patient': patient,
    }
    return render(request, 'rating.html', context)