from rest_framework import generics, permissions
from .models import Prescription
from .serializers import PrescriptionSerializer

class PrescriptionCreateView(generics.CreateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        # You can later trigger a Notification logic here if needed
