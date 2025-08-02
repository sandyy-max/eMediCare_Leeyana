from django.urls import path
from .views import MedicineListView, UploadPrescriptionView, MedicineRequestView, MedicineRequestListView, MedicineRequestDetailView

urlpatterns = [
    path('medicines/', MedicineListView.as_view(), name='medicine-list'),
    path('prescriptions/upload/', UploadPrescriptionView.as_view(), name='upload-prescription'),
    path('request/', MedicineRequestView.as_view(), name='request-medicine'),
    path('requests/', MedicineRequestListView.as_view(), name='medicine-request-list'),
    path('requests/<int:pk>/', MedicineRequestDetailView.as_view(), name='medicine-request-detail'),
]
