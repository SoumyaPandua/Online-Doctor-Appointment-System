from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from website.models import *

def admin_register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        profile_image = request.FILES.get('profile_image')
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('admin_register')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already taken.")
            return redirect('admin_register')

        user = User.objects.create_user(username=email, password=password1)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        admin_profile = AdminProfile.objects.create(
            user=user,
            phone=request.POST.get('phone', ''),
            gender=request.POST.get('gender', ''),
            profile_image=profile_image,
            address=request.POST.get('address', ''),
            is_admin=True
        )
        messages.success(request, "Registration successful.")
        return redirect('admin_login')
    return render(request, 'admin_register.html')

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            try:
                admin_profile = AdminProfile.objects.get(user=user)
                login(request, user)
                request.session['user_id'] = user.id
                request.session['user_name'] = f"{user.first_name} {user.last_name}"
                request.session['user_email'] = user.email
                request.session['role'] = 'admin'
                return redirect('http://127.0.0.1:8000/')
            except AdminProfile.DoesNotExist:
                messages.error(request, "You do not have permission to access the admin panel.")
                return redirect('admin_login')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('admin_login')
    
    return render(request, 'admin_login.html')



def doctor_register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        profile_image = request.FILES.get('profile_image')
        department_id = request.POST.get('department')
        specialization = request.POST['specialization']
        experience = request.POST['experience']
        gender = request.POST.get('gender', 'male')
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('doctor_register')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already taken.")
            return redirect('doctor_register')

        user = User.objects.create_user(username=email, password=password1)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        
        department = Department.objects.get(id=department_id)
        
        doctor_profile = DoctorProfile.objects.create(
            user=user,
            phone=request.POST.get('phone', ''),
            department=department,
            gender=gender,
            specialization=specialization,
            experience=experience,
            profile_image=profile_image,
            address=request.POST.get('address', ''),
            is_doctor=True
        )
        messages.success(request, "Registration successful.")
        return redirect('doctor_login')
    departments = Department.objects.all()
    return render(request, 'doctor_register.html', {'departments': departments})

def doctor_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        
        # Check if the user is a doctor
        if user is not None and hasattr(user, 'doctorprofile'):
            login(request, user)
            doctor_profile = user.doctorprofile
            department_name = doctor_profile.department.name if doctor_profile.department else 'Unknown'

            # Storing information in the session
            request.session['user_id'] = user.id
            request.session['user_name'] = f"{user.first_name} {user.last_name}"
            request.session['user_email'] = user.email
            request.session['role'] = 'doctor'
            request.session['department_name'] = department_name
            
            return redirect('http://127.0.0.1:8000/')
        else:
            messages.error(request, "Invalid credentials or not a doctor.")
            return redirect('doctor_login')
    return render(request, 'doctor_login.html')



def patient_register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        dob = request.POST['dob']
        profile_image = request.FILES.get('image')
        gender = request.POST.get('gender', 'Male')
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('patient_register')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already taken.")
            return redirect('patient_register')

        user = User.objects.create_user(username=email, password=password1)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        
        patient_profile = PatientProfile.objects.create(
            user=user,
            phone=request.POST.get('phone', ''),
            gender=gender,
            dob=dob,
            profile_image=profile_image,
            address=request.POST.get('address', ''),
            is_patient=True
        )
        messages.success(request, "Registration successful.")
        return redirect('patient_login')
    
    return render(request, 'patient_register.html')

def patient_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        
        # Check if the user is a patient
        if user is not None and hasattr(user, 'patientprofile'):
            login(request, user)
            
            # Storing information in the session
            request.session['user_id'] = user.id
            request.session['user_name'] = f"{user.first_name} {user.last_name}"
            request.session['user_email'] = user.email
            request.session['role'] = 'patient'
            return redirect('http://127.0.0.1:8000/')
        else:
            messages.error(request, "Invalid credentials or not a patient.")
            return redirect('patient_login')
    return render(request, 'patient_login.html')



def logout_view(request):
  logout(request)
  return redirect('/')


from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not User.objects.filter(email=email).exists():
            messages.error(request, "User with this email does not exist.")
            return redirect('forgot_password')  # Change to your forgot password URL name

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('forgot_password')

        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        messages.success(request, "Password updated successfully.")
        return redirect('http://127.0.0.1:8000/')

    return render(request, 'forgot_password.html')
