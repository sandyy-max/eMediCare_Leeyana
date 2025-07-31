from django.urls import path
from .views import MedicineListView, UploadPrescriptionView, MedicineRequestView

urlpatterns = [
    path('medicines/', MedicineListView.as_view(), name='medicine-list'),
    path('prescriptions/upload/', UploadPrescriptionView.as_view(), name='upload-prescription'),
    path('request/', MedicineRequestView.as_view(), name='request-medicine'),
]
