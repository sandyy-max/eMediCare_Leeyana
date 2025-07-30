from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Appointment, Confirmation
from .serializers import (
    AppointmentCreateSerializer,
    AppointmentSerializer,
    ConfirmationSerializer,
    PatientAppointmentHistorySerializer
)

# ✅ Book Appointment (Patient View)
class BookAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AppointmentCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Appointment requested successfully. Awaiting confirmation."}, status=status.HTTP_201_CREATED)


# ✅ View Pending Appointments (Admin View)
class PendingAppointmentsView(generics.ListAPIView):
    queryset = Appointment.objects.filter(is_confirmed=False)
    serializer_class = AppointmentSerializer
    permission_classes = [IsAdminUser]


# ✅ Confirm Appointment (Admin View)
class ConfirmAppointmentView(generics.CreateAPIView):
    serializer_class = ConfirmationSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Appointment confirmed successfully."}, status=status.HTTP_201_CREATED)


# ✅ View Patient Appointment History
class PatientAppointmentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patient = request.user
        appointments = Appointment.objects.filter(patient=patient, is_confirmed=True)
        serializer = PatientAppointmentHistorySerializer(appointments, many=True)
        return Response(serializer.data)
