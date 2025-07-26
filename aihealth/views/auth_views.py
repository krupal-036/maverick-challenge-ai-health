from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
import bcrypt

from ..notion.patient_service import PatientService
from ..notion.doctor_service import DoctorService
from ..notion.admin_service import AdminService

def login_view(request):
    if request.session.get('user_id'):
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        patient_service = PatientService()
        doctor_service = DoctorService()
        admin_service = AdminService()
        
        user = patient_service.find_patient_by_email(email)
        role = 'patient'
        
        if not user:
            user = doctor_service.find_doctor_by_email(email)
            role = 'doctor'
        
        if not user:
            user = admin_service.find_admin_by_email(email)
            role = 'mainadmin'
        
        if user:
            if role == 'doctor' and not user['properties']['is_approved']['checkbox']:
                messages.error(request, 'Your account is pending approval by an administrator. Please check back later.')
                return redirect('login')


            password_hash = user['properties']['password_hash']['rich_text'][0]['text']['content']

            if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):

                request.session['user_id'] = user['id'] 
                request.session['user_role'] = role
                request.session['user_name'] = user['properties']['full_name']['rich_text'][0]['text']['content']
                request.session.set_expiry(1209600) 

                messages.success(request, f"Welcome back, {request.session['user_name']}!")
                return redirect('dashboard_redirect')

        messages.error(request, 'Invalid email or password. Please try again.')
        return redirect('login')


    return render(request, 'login.html')

def logout_view(request):

    request.session.flush() 
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')

def dashboard_redirect_view(request):

    if 'user_role' not in request.session:
        messages.error(request, "You must be logged in to view that page.")
        return redirect('login')
    
    role = request.session['user_role']
    if role == 'patient':
        return redirect('patient_dashboard')
    elif role == 'doctor':
        return redirect('doctor_dashboard')
    elif role == 'mainadmin':
        return redirect('admin_dashboard')
    else:

        request.session.flush()
        messages.error(request, "An unknown error occurred. Please log in again.")
        return redirect('login')

def register_dispatch_view(request):

    return render(request, 'registration.html')

def patient_register_view(request):

    if request.method == 'POST':

        data = {
            'full_name': request.POST.get('full_name'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'phone_number': request.POST.get('phone_number'),
            'gender': request.POST.get('gender'),
            'date_of_birth': request.POST.get('date_of_birth'),
            'city': request.POST.get('city'),
        }

        patient_service = PatientService()

        if patient_service.find_patient_by_email(data['email']) or DoctorService().find_doctor_by_email(data['email']):
            messages.error(request, "An account with this email address already exists.")
            return render(request, 'registration_patient.html', {'form_data': data})
        else:

            patient_service.create_patient(data)
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')


    return render(request, 'registration_patient.html')



def doctor_register_view(request):
    """
    Handles the registration form submission for new doctors.
    """
    if request.method == 'POST':

        data = {
            'full_name': request.POST.get('full_name'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'), 
            'phone_number': request.POST.get('phone_number'),
            'medical_registration_number': request.POST.get('medical_registration_number'),
            'specialization': request.POST.get('specialization'),
            'experience_years': request.POST.get('experience_years'),
            'city': request.POST.get('city'),
            'bio': request.POST.get('bio'),
        }


        if not data['password']:
            messages.error(request, "Password cannot be empty.")
            return render(request, 'registration_doctor.html', {'form_data': data})


        doctor_service = DoctorService()
        if doctor_service.find_doctor_by_email(data['email']) or PatientService().find_patient_by_email(data['email']):
            messages.error(request, "An account with this email address already exists.")
            return render(request, 'registration_doctor.html', {'form_data': data})
        else:
            doctor_service.create_doctor(data)
            messages.success(request, 'Registration successful! Your account is now pending review and approval by an administrator.')
            return redirect('login')

    return render(request, 'registration_doctor.html')