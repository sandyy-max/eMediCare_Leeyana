from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Prescription
from .serializers import PrescriptionSerializer

class PrescriptionCreateView(generics.CreateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        # You can later trigger a Notification logic here if needed

class MedicalHistoryView(generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return prescriptions for the logged-in user
        return Prescription.objects.filter(patient=self.request.user).order_by('-prescribed_date')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({
                'message': 'No medical history found.',
                'prescriptions': []
            }, status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Medical history retrieved successfully.',
            'prescriptions': serializer.data
        }, status=status.HTTP_200_OK)
