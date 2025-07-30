from django.urls import path
from .views import PrescriptionCreateView

urlpatterns = [
    path('prescribe/', PrescriptionCreateView.as_view(), name='create-prescription'),
]
