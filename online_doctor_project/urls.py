"""
URL configuration for online_doctor_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from website.views import *
from authapp.views import *
from adminapp.views import *
from doctorapp.views import *
from patientapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', website_view, name='website'),
    path('admin_register/', admin_register, name='admin_register'),
    path('admin_login/', admin_login, name='admin_login'),
    path('doctor_register/', doctor_register, name='doctor_register'),
    path('doctor_login/', doctor_login, name='doctor_login'),
    path('patient_register/', patient_register, name='patient_register'),
    path('patient_login/', patient_login, name='patient_login'),
    path('admin_dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('doctor_dashboard/', doctor_dashboard_view, name='doctor_dashboard'),
    path('admin_profile/', admin_profile_view, name='admin_profile'),
    path('doctor_profile/', doctor_profile_view, name='doctor_profile'),
    path('patient_profile/', patient_profile_view, name='patient_profile'),
    path('doctor_timing/', doctor_timing_view, name='doctor_timing'),
    path('add_timing/', add_timing_view, name='add_timing'),
    path('update_timing/<int:pk>/', update_timing_view, name='update_timing'),
    path('delete_timing/<int:pk>/', delete_timing_view, name='delete_timing'),
    path('departments_list/', department_list_view, name='department_list'),
    path('add_departments/', add_department_view, name='add_departments'),
    path('edit_department/<int:department_id>/', edit_department_view, name='edit_department'),
    path('delete_department/<int:department_id>/', delete_department_view, name='delete_department'),
    path('website-setting/', website_setting_view, name='website_setting'),
    path('department/<str:department_name>/', department_detail_view, name='department_detail'),
    path('readmore_doctor/<int:doctor_id>/', readmore_doctor_view, name='readmore_doctor'),
    path('doctor/<int:doctor_id>/booking/', doctor_booking_view, name='doctor_booking'),
    path('calcucalculate_age/',calculate_age_view, name='calculate_age'),
    path('today_appointments/', today_appointments_view, name="today_appointments"),
    path('view_appointments/<str:apt_no>/', view_appointments_view, name="view_appointments"),
    path('appointment_history/',appointment_history_view, name='appointment_history'),
    path('patient_update_password/', patient_update_password, name='patient_update_password'),
    path('doctor_update_password/', doctor_update_password, name='doctor_update_password'),
    path('admin_update_password/', admin_update_password, name='admin_update_password'),
    path('logout/', logout_view, name='logout'),
    path('rating/', rating_view, name='rating'),
    path('doctor_appointments/', doctor_appointments_view, name='doctor_appointments'),
    path('appointment/<str:apt_no>/', patient_view, name='patient_view'),
    path('all_appointments/', all_appointments_view, name='all_appointments'),
    path('doctor_patient_list/', doctor_patient_list_view, name='doctor_patient_list'),
    path('forgot_password/', forgot_password_view, name='forgot_password'),
    path('admin_appointments/', admin_appointments, name='admin_appointments'),
    path('admin_appointment_view/<str:apt_no>/', admin_appointment_view, name='admin_appointment_view'),
    path('admin_appointments_history/', admin_appointments_history, name='admin_appointments_history'),
    path('admin_doctor_list', admin_doctor_list_view, name='admin_doctor_list'),
    path('admin_patient_list', admin_patient_list_view, name='admin_patient_list'),
    path('add-doctor/', add_doctor, name='add_doctor'),
    path('add-patient/', add_patient, name='add_patient'),
    path('patients_list/', patients_list, name='patients_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
