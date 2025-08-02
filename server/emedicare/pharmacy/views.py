from rest_framework import generics, permissions, status, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Medicine, Prescription, MedicineRequest
from .serializer import MedicineSerializer, PrescriptionSerializer, MedicineRequestSerializer

class MedicineListView(generics.ListAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [permissions.AllowAny]

class UploadPrescriptionView(generics.CreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

class MedicineRequestView(generics.CreateAPIView):
    serializer_class = MedicineRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)
    
    def create(self, request, *args, **kwargs):
        print(f"Medicine request received: {request.data}")
        print(f"Content-Type: {request.content_type}")
        return super().create(request, *args, **kwargs)

class MedicineRequestListView(generics.ListAPIView):
    serializer_class = MedicineRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            # Admin can see all requests
            return MedicineRequest.objects.all()
        else:
            # Patients can only see their own requests
            return MedicineRequest.objects.filter(patient=user)

class MedicineRequestDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = MedicineRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return MedicineRequest.objects.all()
        else:
            return MedicineRequest.objects.filter(patient=user)
    
    def update(self, request, *args, **kwargs):
        # Only admin can update status and add notes
        if request.user.role != 'admin':
            return Response(
                {"error": "Only administrators can update medicine requests"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
