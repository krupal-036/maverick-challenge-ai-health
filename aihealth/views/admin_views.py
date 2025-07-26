from django.shortcuts import render, redirect
from django.contrib import messages
from ..notion.doctor_service import DoctorService
from ..notion.patient_service import PatientService

def admin_dashboard(request):
    if request.session.get('user_role') != 'mainadmin':
        return redirect('login')

    doctor_service = DoctorService()
    patient_service = PatientService()

    all_doctors = doctor_service.get_all_doctors()
    all_patients = patient_service.get_all_patients()

    unapproved_doctors = [d for d in all_doctors if not d['properties']['is_approved']['checkbox']]

    context = {
        'unapproved_doctors': unapproved_doctors,
        'all_doctors': all_doctors,
        'all_patients': all_patients,
        'user_name': request.session.get('user_name')
    }
    return render(request, 'admin_dashboard.html', context)

def approve_doctor(request, doctor_id):
    if request.session.get('user_role') != 'mainadmin':
        return redirect('login')
    
    doctor_service = DoctorService()
    doctor_service.approve_doctor_account(doctor_id)
    messages.success(request, 'Doctor account has been approved.')
    return redirect('admin_dashboard')

def delete_user(request, role, user_id):
    if request.session.get('user_role') != 'mainadmin':
        return redirect('login')
    
    if role == 'doctor':
        service = DoctorService()
    elif role == 'patient':
        service = PatientService()
    else:
        messages.error(request, "Invalid user role.")
        return redirect('admin_dashboard')

    service.delete_page(user_id)
    messages.success(request, f"The {role} has been deleted.")
    return redirect('admin_dashboard')