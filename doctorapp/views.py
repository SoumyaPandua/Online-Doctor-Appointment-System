from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from website.models import *
from authapp.models import *
from .models import *
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def doctor_dashboard_view(request):
    doctor = DoctorProfile.objects.get(user=request.user)
    total_appointments = Appointment.objects.filter(doctor=doctor).count()
    completed_appointments = Appointment.objects.filter(doctor=doctor, status='completed').count()
    future_appointments = Appointment.objects.filter(doctor=doctor, status='booked', apt_date__gt=date.today()).count()
    context = {
        'total_appointments': total_appointments,
        'completed_appointments': completed_appointments,
        'future_appointments': future_appointments,
    }
    return render(request, 'doctor_dashboard.html', context)

@login_required
def doctor_profile_view(request):
    doctor_user = DoctorProfile.objects.get(user_id=request.user.id)
    
    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        profile_image = request.FILES.get('doctor-image')
        department_id = request.POST.get('department')
        designation = request.POST.get('designation')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        specialization = request.POST.get('specialization')
        bio = request.POST.get('bio')
        consultant_fees = request.POST.get('consultant-fees')

        # Update user information
        doctor_user.user.first_name = first_name
        doctor_user.user.last_name = last_name
        doctor_user.user.save()

        # Update profile information
        if phone:
            doctor_user.phone = phone
        if address:
            doctor_user.address = address
        if gender:
            doctor_user.gender = gender
        if profile_image:
            doctor_user.profile_image = profile_image
        if department_id:
            department = Department.objects.get(id=department_id)
            doctor_user.department = department
        if designation:
            doctor_user.designation = designation
        if qualification:
            doctor_user.qualification = qualification
        if experience:
            doctor_user.experience = experience
        if specialization:
            doctor_user.specialization = specialization
        if bio:
            doctor_user.bio = bio
        if consultant_fees:
            doctor_user.consultant_fees = consultant_fees

        doctor_user.save()
        request.session['user_name'] = f"{doctor_user.user.first_name} {doctor_user.user.last_name}"
        request.session['department_name'] = doctor_user.department.name if doctor_user.department else None
        return redirect('doctor_profile')

    doctor_details = {
        'first_name': doctor_user.user.first_name,
        'last_name': doctor_user.user.last_name,
        'email': doctor_user.user.email,  # Email is not editable
        'phone': doctor_user.phone,
        'address': doctor_user.address,
        'gender': doctor_user.gender,
        'profile_image': doctor_user.profile_image.url if doctor_user.profile_image else None,
        'department': doctor_user.department.id if doctor_user.department else None,
        'designation': doctor_user.designation,
        'qualification': doctor_user.qualification,
        'experience': doctor_user.experience,
        'specialization': doctor_user.specialization,
        'bio': doctor_user.bio,
        'consultant_fees': doctor_user.consultant_fees,
    }
    departments = Department.objects.all()
    return render(request, 'doctor_profile.html', {'doctor_details': doctor_details, 'departments': departments})


def doctor_timing_view(request):
    try:
        doctor_profile = request.user.doctorprofile
    except DoctorProfile.DoesNotExist:
        return redirect('doctor_login')
    timings = DoctorTimetable.objects.filter(doctor=doctor_profile)
    return render(request, 'doctor_timing.html', {'timings': timings})

@login_required
def add_timing_view(request):
    try:
        doctor_profile = request.user.doctorprofile
    except DoctorProfile.DoesNotExist:
        return redirect('doctor_login')
    if request.method == 'POST':
        day = request.POST.get('day')
        shift = request.POST.get('shift')
        start_time = request.POST.get('startTime')
        end_time = request.POST.get('endTime')
        avg_consult_time = int(request.POST.get('avg_consult_time'))

        if DoctorTimetable.objects.filter(doctor=doctor_profile, day=day, shift=shift).exists():
            return redirect('doctor_timing')
        DoctorTimetable.objects.create(
            doctor=doctor_profile,
            day=day,
            shift=shift,
            start_time=start_time,
            end_time=end_time,
            avg_consult_time=avg_consult_time,
        )
        return redirect('doctor_timing')
    return redirect('doctor_timing')

@login_required
def update_timing_view(request, pk):
    try:
        doctor_profile = request.user.doctorprofile
    except DoctorProfile.DoesNotExist:
        return redirect('doctor_login')
    timing = get_object_or_404(DoctorTimetable, pk=pk, doctor=doctor_profile)
    if request.method == 'POST':
        start_time = request.POST.get('start-time')
        end_time = request.POST.get('end-time')
        avg_consult_time = int(request.POST.get('avg-consult-time'))

        timing.start_time = start_time
        timing.end_time = end_time
        timing.avg_consult_time = avg_consult_time
        timing.save()
        return redirect('doctor_timing')
    context = {
        'timing': timing,
    }
    return render(request, 'update_timing.html', context)


@login_required
def delete_timing_view(request, pk):
    try:
        doctor_profile = request.user.doctorprofile
    except DoctorProfile.DoesNotExist:
        return redirect('doctor_login')
    timing = get_object_or_404(DoctorTimetable, pk=pk, doctor=doctor_profile)
    timing.delete()
    return redirect('doctor_timing')

@login_required
def doctor_appointments_view(request):
    doctor = request.user.doctorprofile
    appointments = Appointment.objects.filter(doctor=doctor)
    return render(request, 'doctor_appointments.html', {'appointments': appointments})

@login_required
def patient_view(request, apt_no):
    appointment = get_object_or_404(Appointment, apt_no=apt_no)
    
    if request.method == 'POST':
        if hasattr(request.user, 'doctorprofile') and request.user.doctorprofile == appointment.doctor:
            appointment.status = request.POST.get('status')
            appointment.consultation_status = request.POST.get('consultation-status')
            appointment.consultation_fees = request.POST.get('fees')
            appointment.doctor_comment = request.POST.get('doctor-comment')
            appointment.save()
        else:
            return redirect('patient_view')
    
    return render(request, 'patient_view.html', {'appointment': appointment})

@login_required
def all_appointments_view(request):
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-apt_date')

    return render(request, 'all_appointments.html', {
        'appointments': appointments
    })


@login_required
def doctor_update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not current_password:
            messages.error(request, "Current password is required.")
            return redirect('doctor_update_password')

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('doctor_update_password')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('doctor_update_password')

        if current_password == new_password:
            messages.error(request, "New password cannot be the same as the current password.")
            return redirect('doctor_update_password')

        user = request.user
        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)
        messages.success(request, "Password updated successfully.")
        return redirect('doctor_profile')

    return render(request, 'doctor_update_password.html')

@login_required
def doctor_patient_list_view(request):
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    patients = PatientProfile.objects.filter(appointment__doctor=doctor).distinct()

    return render(request, 'my_patients.html', {'patients': patients})