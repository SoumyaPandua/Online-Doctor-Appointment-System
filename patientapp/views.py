from django.shortcuts import render, redirect
from datetime import datetime, date
from authapp.models import PatientProfile
from doctorapp.models import Appointment
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils import timezone

@login_required
def patient_profile_view(request):
    user = request.user
    try:
        patient_profile = user.patientprofile
    except PatientProfile.DoesNotExist:
        return redirect('patient_login')

    if not request.session.get('first_name'):
        request.session['first_name'] = patient_profile.user.first_name
    if not request.session.get('last_name'):
        request.session['last_name'] = patient_profile.user.last_name
    if not request.session.get('phone'):
        request.session['phone'] = patient_profile.phone
    if not request.session.get('email'):
        request.session['email'] = patient_profile.user.email
    if not request.session.get('gender'):
        request.session['gender'] = patient_profile.gender
    if not request.session.get('dob'):
        request.session['dob'] = patient_profile.dob.strftime('%Y-%m-%d') if patient_profile.dob else ''
    if not request.session.get('profile_image'):
        request.session['profile_image'] = patient_profile.profile_image.url if patient_profile.profile_image else ''
    if not request.session.get('address'):
        request.session['address'] = patient_profile.address

    if request.method == 'POST':
        patient_profile.user.first_name = request.POST.get('first_name', patient_profile.user.first_name)
        patient_profile.user.last_name = request.POST.get('last_name', patient_profile.user.last_name)
        patient_profile.phone = request.POST.get('phone', patient_profile.phone)
        patient_profile.gender = request.POST.get('gender', patient_profile.gender)
        patient_profile.address = request.POST.get('patient_address', patient_profile.address)
        
        dob_str = request.POST.get('dob', None)
        if dob_str:
            try:
                patient_profile.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        if 'profile_image' in request.FILES:
            patient_profile.profile_image = request.FILES['profile_image']
        patient_profile.user.save()
        patient_profile.save()
        request.session['first_name'] = patient_profile.user.first_name
        request.session['last_name'] = patient_profile.user.last_name
        request.session['phone'] = patient_profile.phone
        request.session['gender'] = patient_profile.gender
        request.session['dob'] = patient_profile.dob.strftime('%Y-%m-%d') if isinstance(patient_profile.dob, date) else patient_profile.dob
        request.session['profile_image'] = patient_profile.profile_image.url if patient_profile.profile_image else ''
        request.session['address'] = patient_profile.address
        return redirect('patient_profile')
    context = {
        'patient_session_details': {
            'first_name': request.session['first_name'],
            'last_name': request.session['last_name'],
            'phone': request.session['phone'],
            'email': request.session['email'],
            'gender': request.session['gender'],
            'dob': request.session['dob'],
            'profile_image': request.session['profile_image'],
            'address': request.session['address'],
        }
    }
    return render(request, 'patient_profile.html', context)


@login_required
def today_appointments_view(request):
    patient = request.user.patientprofile
    appointments = Appointment.objects.filter(patient=patient)
    return render(request, 'today_appointments.html', {'appointments': appointments})

from django.shortcuts import render, get_object_or_404
from authapp.models import *

@login_required
def view_appointments_view(request, apt_no):
    appointment = get_object_or_404(Appointment, apt_no=apt_no)
    doctor_profile = appointment.doctor
    patient_profile = appointment.patient

    context = {
        'appointment': appointment,
        'doctor_profile': doctor_profile,
        'patient_profile': patient_profile,
    }
    return render(request, 'view_appointment.html', context)

@login_required
def appointment_history_view(request):
    patient = request.user.patientprofile
    appointments = Appointment.objects.filter(patient=patient)
    context = {
        'appointments': appointments,
    }
    return render(request, 'appointment_history.html', context)



@login_required
def patient_update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not current_password:
            messages.error(request, "Current password is required.")
            return redirect('update_password')

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('update_password')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('update_password')

        if current_password == new_password:
            messages.error(request, "New password cannot be the same as the current password.")
            return redirect('update_password')

        user = request.user
        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)
        messages.success(request, "Password updated successfully.")
        return redirect('patient_profile')

    return render(request, 'update_password.html')
