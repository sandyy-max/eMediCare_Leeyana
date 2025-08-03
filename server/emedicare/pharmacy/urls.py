from django.urls import path
from .views import (
    MedicineListView, UploadPrescriptionView, MedicineRequestView, 
    MedicineRequestListView, MedicineRequestDetailView,
    AdminMedicineRequestListView, AdminMedicineRequestDetailView, MedicineRequestStatsView
)

urlpatterns = [
    path('medicines/', MedicineListView.as_view(), name='medicine-list'),
    path('prescriptions/upload/', UploadPrescriptionView.as_view(), name='upload-prescription'),
    path('request/', MedicineRequestView.as_view(), name='request-medicine'),
    path('requests/', MedicineRequestListView.as_view(), name='medicine-request-list'),
    path('requests/<int:pk>/', MedicineRequestDetailView.as_view(), name='medicine-request-detail'),
    
    # Admin endpoints
    path('admin/requests/', AdminMedicineRequestListView.as_view(), name='admin-medicine-request-list'),
    path('admin/requests/<int:pk>/', AdminMedicineRequestDetailView.as_view(), name='admin-medicine-request-detail'),
    path('admin/stats/', MedicineRequestStatsView.as_view(), name='medicine-request-stats'),
]
