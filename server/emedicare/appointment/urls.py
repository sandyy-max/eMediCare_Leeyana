from django.urls import path
from .views import PatientAppointmentHistoryView
from .views import (
    BookAppointmentView,
    PendingAppointmentsView,
    ConfirmAppointmentView,
)

urlpatterns = [
    path('book/', BookAppointmentView.as_view(), name='book-appointment'),
    path('pending/', PendingAppointmentsView.as_view(), name='pending-appointments'),
    path('confirm/', ConfirmAppointmentView.as_view(), name='confirm-appointment'),
    path('my-appointments/', PatientAppointmentHistoryView.as_view(), name='my-appointments'),
    path('book-appointment/', BookAppointmentView.as_view(), name='book-appointment'),
]
