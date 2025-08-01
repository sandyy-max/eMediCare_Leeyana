from django.urls import path
from .views import PrescriptionCreateView, MedicalHistoryView

urlpatterns = [
    path('prescribe/', PrescriptionCreateView.as_view(), name='create-prescription'),
    path('history/', MedicalHistoryView.as_view(), name='medical-history'),
]
