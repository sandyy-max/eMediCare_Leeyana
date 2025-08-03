from django.urls import path
from .views import (
    BookAppointmentView,
    PendingAppointmentsView,
    ConfirmAppointmentView,
    PatientAppointmentHistoryView,
    PatientUpcomingAppointmentsView,
    DoctorsByDepartmentView,
    RejectAppointmentView
)

urlpatterns = [
    path('', BookAppointmentView.as_view(), name='book-appointment'),
    path('pending/', PendingAppointmentsView.as_view(), name='pending-appointments'),
    path('confirm/', ConfirmAppointmentView.as_view(), name='confirm-appointment'),
    path('reject/<int:appointment_id>/', RejectAppointmentView.as_view(), name='reject-appointment'),
    path('my-appointments/', PatientAppointmentHistoryView.as_view(), name='my-appointments'),
    path('upcoming/', PatientUpcomingAppointmentsView.as_view(), name='upcoming-appointments'),
    path('doctors/', DoctorsByDepartmentView.as_view(), name='doctors-by-department'),
]
