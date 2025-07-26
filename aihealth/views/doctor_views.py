from django.shortcuts import render, redirect
from django.contrib import messages
from ..notion.consultation_service import ConsultationService
from datetime import datetime

def doctor_dashboard(request):

    if request.session.get('user_role') != 'doctor':
        return redirect('login')

    doctor_id = request.session.get('user_id')
    consultation_service = ConsultationService()


    raw_pending_requests = consultation_service.get_consultations_for_doctor(doctor_id)
    

    processed_requests = []
    for item in raw_pending_requests:
        properties = item.get('properties', {})
        
        request_page_id = item.get('id', '')

        patient_name_obj = properties.get('patient_name', {}).get('rich_text', [])
        patient_name = patient_name_obj[0].get('text', {}).get('content', 'N/A') if patient_name_obj else 'N/A'

        date_obj = properties.get('request_date', {}).get('date')
        request_date_formatted = "N/A"
        if date_obj and date_obj.get('start'):
            try:

                date_val = datetime.fromisoformat(date_obj['start'])
                request_date_formatted = date_val.strftime('%b. %d, %Y at %I:%M %p') 
            except (ValueError, TypeError):
                request_date_formatted = "Invalid Date"
        
        processed_requests.append({
            'request_page_id': request_page_id,
            'patient_name': patient_name,
            'request_date_formatted': request_date_formatted,
        })

    context = {
        'pending_requests': processed_requests,
        'user_name': request.session.get('user_name')
    }
    return render(request, 'doctor_dashboard.html', context)

def handle_consultation(request, request_id, action):

    if request.session.get('user_role') != 'doctor':
        return redirect('login')

    consultation_service = ConsultationService()

    if action.lower() in ['accepted', 'rejected']:
        consultation_service.update_consultation_status(request_id, action.capitalize())
        messages.success(request, f"Request has been successfully {action}.")
    else:
        messages.error(request, "An invalid action was performed.")
        
    return redirect('doctor_dashboard')