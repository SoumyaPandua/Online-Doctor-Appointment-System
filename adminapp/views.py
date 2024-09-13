from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from website.models import *
from authapp.models import *
from doctorapp.models import *
from django.contrib.auth import update_session_auth_hash

def admin_dashboard_view(request):
    today = date.today()
    total_appointments_count = Appointment.objects.count()
    today_appointments_count = Appointment.objects.filter(status='booked', apt_date=today).count()
    completed_appointments_count = Appointment.objects.filter(status='completed').count()
    future_appointments_count = Appointment.objects.filter(status='booked', apt_date__gt=today).count()
    total_departments_count = Department.objects.count()
    total_doctors_count = DoctorProfile.objects.count()
    total_admins_count = AdminProfile.objects.count()
    total_patients_count = PatientProfile.objects.count()
    context = {
        'total_appointments_count': total_appointments_count,
        'today_appointments_count': today_appointments_count,
        'completed_appointments_count': completed_appointments_count,
        'future_appointments_count': future_appointments_count,
        'total_departments_count': total_departments_count,
        'total_doctors_count': total_doctors_count,
        'total_admins_count': total_admins_count,
        'total_patients_count': total_patients_count,
    }
    return render(request, 'admin_dashboard.html', context)

def department_list_view(request):
    departments = Department.objects.all()
    return render(request, 'departments.html', {'departments': departments})

def add_department_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        image = request.FILES['image']

        department = Department(name=name, image=image)
        department.save()
        return redirect('department_list')

    return render(request, 'add_departments.html')

def edit_department_view(request, department_id):
    department = get_object_or_404(Department, pk=department_id)

    if request.method == 'POST':
        department.name = request.POST['name']
        if 'image' in request.FILES:
            department.image = request.FILES['image']
        department.save()
        return redirect('department_list')

    return render(request, 'edit_department.html', {'department': department})

def delete_department_view(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    department.delete()
    return redirect('department_list')


@login_required
def admin_profile_view(request):
    try:
        admin_user = AdminProfile.objects.get(user=request.user)
    except AdminProfile.DoesNotExist:
        return redirect('admin_login')

    if request.method == 'POST':
        first_name = request.POST.get('first-name', admin_user.user.first_name)
        last_name = request.POST.get('last-name', admin_user.user.last_name)
        phone = request.POST.get('phone', admin_user.phone)
        address = request.POST.get('address', admin_user.address)
        gender = request.POST.get('gender', admin_user.gender)
        profile_image = request.FILES.get('image', admin_user.profile_image)

        # Update user details
        admin_user.user.first_name = first_name
        admin_user.user.last_name = last_name
        admin_user.user.save()
        
        # Update profile details
        admin_user.phone = phone
        admin_user.address = address
        admin_user.gender = gender
        if profile_image:
            admin_user.profile_image = profile_image
        
        admin_user.save()

        # Update session data
        request.session['user_name'] = f"{admin_user.user.first_name} {admin_user.user.last_name}"
        request.session['user_email'] = admin_user.user.email
        request.session['phone'] = admin_user.phone
        request.session['address'] = admin_user.address
        request.session['gender'] = admin_user.gender
        request.session['profile_image'] = admin_user.profile_image.url if admin_user.profile_image else None

        return redirect('admin_profile')

    admin_details = {
        'first_name': admin_user.user.first_name,
        'last_name': admin_user.user.last_name,
        'email': admin_user.user.email,  # Email is not editable
        'phone': admin_user.phone,
        'address': admin_user.address,
        'gender': admin_user.gender,
        'profile_image': admin_user.profile_image.url if admin_user.profile_image else None,
    }
    return render(request, 'admin_profile.html', {'admin_details': admin_details})



def website_setting_view(request):
    # Fetch the first WebsiteContent object or create a new one if it doesn't exist
    content, created = WebsiteContent.objects.get_or_create(pk=1)  # Use a default pk value
    faqs = FAQ.objects.all()

    if request.method == "POST":
        if content:
            content.title = request.POST.get('title', content.title)
            content.copyright_text = request.POST.get('copyright_text', content.copyright_text)
            content.address_line1 = request.POST.get('address_line1', content.address_line1)
            content.address_line2 = request.POST.get('address_line2', content.address_line2)
            content.phone_number = request.POST.get('phone_number', content.phone_number)
            content.email = request.POST.get('email', content.email)
            content.about_text = request.POST.get('about_text', content.about_text)
            content.domain = request.POST.get('domain', content.domain)

            if request.FILES.get('logo_image'):
                content.logo_image = request.FILES['logo_image']

            if request.FILES.get('favicon'):
                content.favicon = request.FILES['favicon']
            
            if request.FILES.get('faq_image'):
                content.faq_image = request.FILES['faq_image']
            content.save()
        new_question = request.POST.get('new_question')
        new_answer = request.POST.get('new_answer')

        if new_question and new_answer:
            FAQ.objects.create(question=new_question, answer=new_answer)

        return redirect('website_setting')

    return render(request, 'website_setting.html', {'content': content, 'faqs': faqs})


from django.contrib import messages
from doctorapp.models import *

@login_required
def admin_appointments(request):
    appointments = Appointment.objects.all()
    context = {
        'appointments': appointments
    }
    return render(request, 'admin_appointments.html', context)

@login_required
def admin_appointment_view(request, apt_no):
    appointment = get_object_or_404(Appointment, apt_no=apt_no)
    context = {
        'appointment': appointment
    }
    return render(request, 'admin_appointment_view.html', context)

@login_required
def delete_appointment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    messages.success(request, "Appointment deleted successfully.")
    return redirect('admin_appointments')


from django.utils.dateparse import parse_date
from datetime import timedelta

@login_required
def admin_appointments_history(request):
    # Handle filtering based on the month
    month = request.GET.get('month')
    if month:
        try:
            # Parse the month into a date range
            start_date = parse_date(f'{month}-01')
            end_date = start_date.replace(day=28) + timedelta(days=4)  # This will always get us to the end of the month
            end_date = end_date - timedelta(days=end_date.day)
            appointments = Appointment.objects.filter(apt_date__range=[start_date, end_date])
        except ValueError:
            appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.all()
    
    context = {
        'appointments': appointments,
    }
    return render(request, 'admin_appointments_history.html', context)


def admin_doctor_list_view(request):
    doctors = DoctorProfile.objects.filter(is_doctor=True)
    return render(request, 'admin_doctor_list.html', {'doctors': doctors})


def add_doctor(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        department_id = request.POST.get('department')
        gender = request.POST.get('gender')
        designation = request.POST.get('designation')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience') or 0
        specialization = request.POST.get('specialization') or ''
        bio = request.POST.get('bio') or ''
        consultant_fees = request.POST.get('consultant-fees') or 0.00
        address = request.POST.get('address') or ''
        profile_image = request.FILES.get('doctor-image')

        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except Exception as e:
            return render(request, 'add_doctor.html', {'error': f'Error creating user: {e}', 'departments': departments})

        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            user.delete()
            return render(request, 'add_doctor.html', {'error': 'Selected department does not exist', 'departments': departments})

        try:
            DoctorProfile.objects.create(
                user=user,
                phone=phone,
                department=department,
                gender=gender,
                designation=designation,
                qualification=qualification,
                experience=experience,
                specialization=specialization,
                bio=bio,
                consultant_fees=consultant_fees,
                profile_image=profile_image,
                address=address,
                is_doctor=True,
            )
        except Exception as e:
            user.delete()
            return render(request, 'add_doctor.html', {'error': f'Error creating doctor profile: {e}', 'departments': departments})

        return redirect('admin_doctor_list')

    return render(request, 'add_doctor.html', {'departments': departments})


@login_required
def patients_list(request):
    selected_doctor_id = request.GET.get('doctor')
    doctors = DoctorProfile.objects.filter(is_active=True)
    
    if selected_doctor_id:
        patients = PatientProfile.objects.filter(appointment__doctor_id=selected_doctor_id).distinct()
    else:
        patients = PatientProfile.objects.none()

    context = {
        'doctors': doctors,
        'patients': patients,
        'selected_doctor_id': selected_doctor_id,
    }
    return render(request, 'patients.html', context)


def add_patient(request):
    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        profile_image = request.FILES.get('profile_image')

        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except Exception as e:
            return render(request, 'add_patient.html', {'error': f'Error creating user: {e}'})

        try:
            PatientProfile.objects.create(
                user=user,
                phone=phone or '',
                gender=gender,
                dob=dob,
                profile_image=profile_image,
                address=address or '',
                is_patient=True
            )
        except Exception as e:
            user.delete()
            return render(request, 'add_patient.html', {'error': f'Error creating patient profile: {e}'})
        return redirect('admin_patient_list')
    return render(request, 'add_patient.html')


@login_required
def admin_update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not current_password:
            messages.error(request, "Current password is required.")
            return redirect('admin_update_password')

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('admin_update_password')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('admin_update_password')

        if current_password == new_password:
            messages.error(request, "New password cannot be the same as the current password.")
            return redirect('admin_update_password')

        user = request.user
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Password updated successfully.")
        return redirect('admin_profile')
    return render(request, 'admin_update_password.html')

def admin_patient_list_view(request):
    patients = PatientProfile.objects.filter(is_patient=True)
    return render(request, 'admin_patient_list.html', {'patients': patients})