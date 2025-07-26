import markdown
from django.shortcuts import render, redirect
from django.contrib import messages
from ..notion.doctor_service import DoctorService 
from ..notion.consultation_service import ConsultationService
from ..gemini.gemini_chatbot import GeminiChatbot
from datetime import datetime

def patient_dashboard(request):
    if request.session.get('user_role') != 'patient':
        return redirect('login')
    
    patient_id = request.session.get('user_id')
    consultation_service = ConsultationService()
    doctor_service = DoctorService()

    raw_consultations = consultation_service.get_consultations_for_patient(patient_id)
    approved_doctors = doctor_service.get_all_doctors(approved_only=True)

    processed_consultations = []
    for item in raw_consultations:
        properties = item.get('properties', {})

        doctor_name_obj = properties.get('doctor_name', {}).get('rich_text', [])
        doctor_name = doctor_name_obj[0].get('text', {}).get('content', 'N/A') if doctor_name_obj else 'N/A'

        status = properties.get('status', {}).get('select', {}).get('name', 'N/A')

        date_obj = properties.get('request_date', {}).get('date')
        request_date_formatted = "N/A"
        if date_obj and date_obj.get('start'):
            try:
                date_val = datetime.fromisoformat(date_obj['start'])
                request_date_formatted = date_val.strftime('%b. %d, %Y') 
            except (ValueError, TypeError):
                request_date_formatted = "Invalid Date"

        processed_consultations.append({
            'doctor_name': doctor_name,
            'status': status,
            'request_date_formatted': request_date_formatted,
        })


    context = {
        'consultations': processed_consultations, 
        'doctors': approved_doctors,
        'user_name': request.session.get('user_name'),
        'diagnosis': request.session.pop('diagnosis', None) 
    }
    return render(request, 'patient_dashboard.html', context)

def chatbot_view(request):
    if request.session.get('user_role') != 'patient':
        return redirect('login')

    if request.method == 'POST':
        symptoms = request.POST.get('symptoms')
        if symptoms:
            chatbot = GeminiChatbot()
            raw_diagnosis = chatbot.get_diagnosis(symptoms)

            html_diagnosis = markdown.markdown(raw_diagnosis)

            request.session['diagnosis'] = html_diagnosis
        else:
            messages.error(request, "Please describe your symptoms.")
    
    return redirect('patient_dashboard')

def request_consultation(request):
    if request.session.get('user_role') != 'patient' or request.method != 'POST':
        return redirect('patient_dashboard')
    
    doctor_service = DoctorService()
    consultation_service = ConsultationService()

    doctor_id = request.POST.get('doctor_id')
    if not doctor_id:
        messages.error(request, "You must select a doctor.")
        return redirect('patient_dashboard')

    patient_id = request.session.get('user_id')
    patient_name = request.session.get('user_name')

    all_doctors = doctor_service.get_all_doctors(approved_only=True)
    doctor_name = "Unknown"
    for doc in all_doctors:
        if doc['id'] == doctor_id:
            doctor_name = doc['properties']['full_name']['rich_text'][0]['text']['content']
            break

    consultation_service.create_consultation_request(patient_id, doctor_id, patient_name, doctor_name)
    messages.success(request, "Consultation request sent successfully!")
    return redirect('patient_dashboard')







