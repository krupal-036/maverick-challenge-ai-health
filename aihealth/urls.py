from django.contrib import admin
from django.urls import path
from .views import auth_views, patient_views, doctor_views, admin_views

urlpatterns = [
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('register/', auth_views.register_dispatch_view, name='register_dispatch'),
    path('register/patient/', auth_views.patient_register_view, name='register_patient'),
    path('register/doctor/', auth_views.doctor_register_view, name='register_doctor'),

    path('', auth_views.dashboard_redirect_view, name='dashboard_redirect'),

    path('patient/dashboard/', patient_views.patient_dashboard, name='patient_dashboard'),
    path('patient/chatbot/', patient_views.chatbot_view, name='chatbot'),
    path('patient/request-consultation/', patient_views.request_consultation, name='request_consultation'),

    path('doctor/dashboard/', doctor_views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/consultation/<str:request_id>/<str:action>/', doctor_views.handle_consultation, name='handle_consultation'),

    path('admin/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin/approve-doctor/<str:doctor_id>/', admin_views.approve_doctor, name='approve_doctor'),
    path('admin/delete-user/<str:role>/<str:user_id>/', admin_views.delete_user, name='delete_user'),
]