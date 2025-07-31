from rest_framework import generics, permissions
from .models import Medicine, Prescription, MedicineRequest
from .serializer import MedicineSerializer, PrescriptionSerializer, MedicineRequestSerializer

class MedicineListView(generics.ListAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAuthenticated]

class UploadPrescriptionView(generics.CreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

class MedicineRequestView(generics.CreateAPIView):
    serializer_class = MedicineRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)
