from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Appointment, Confirmation, Doctor
from .serializers import (
    AppointmentCreateSerializer,
    AppointmentSerializer,
    ConfirmationSerializer,
    PatientAppointmentHistorySerializer,
    DoctorSerializer
)

# ✅ Book Appointment (Patient View)
class BookAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AppointmentCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()
        
        # Create notification for admin
        from notification.models import Notification
        from userauth.models import User
        
        admin_notification_title = f"New Appointment Request - {appointment.department}"
        admin_notification_message = f"""
        Patient: {appointment.full_name}
        Department: {appointment.department}
        Phone: {appointment.phone_number}
        Email: {appointment.email}
        Symptoms: {appointment.symptoms}
        Date of Birth: {appointment.dob}
        
        Please review and confirm this appointment.
        """
        
        # Send notification to all admin users
        admin_users = User.objects.filter(role='admin')
        for admin_user in admin_users:
            Notification.objects.create(
                patient=admin_user,
                title=admin_notification_title,
                message=admin_notification_message,
                notification_type='appointment',
                related_id=appointment.id
            )
        
        # Create notification for patient
        patient_notification_title = "Appointment Request Submitted"
        patient_notification_message = f"""
        Your appointment request for {appointment.department} has been submitted successfully.
        
        We will review your request and contact you shortly to confirm your appointment.
        Please keep your phone available for our call.
        """
        
        Notification.objects.create(
            patient=request.user,
            title=patient_notification_title,
            message=patient_notification_message,
            notification_type='appointment',
            related_id=appointment.id
        )
        
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
        confirmation = serializer.save()
        
        # Create notification for patient
        from notification.models import Notification
        
        patient_notification_title = "Appointment Confirmed"
        patient_notification_message = f"""
        Your appointment has been confirmed!
        
        Department: {confirmation.appointment.department}
        Doctor: {confirmation.doctor.name}
        Date: {confirmation.appointment_date}
        Time: {confirmation.appointment_time}
        
        Please arrive 15 minutes before your scheduled time.
        If you need to reschedule, please contact us at least 24 hours in advance.
        """
        
        Notification.objects.create(
            patient=confirmation.appointment.patient,
            title=patient_notification_title,
            message=patient_notification_message,
            notification_type='appointment',
            related_id=confirmation.appointment.id
        )
        
        # Create notification for admin (confirmation record)
        admin_notification_title = f"Appointment Confirmed - {confirmation.appointment.full_name}"
        admin_notification_message = f"""
        Appointment confirmed successfully:
        
        Patient: {confirmation.appointment.full_name}
        Department: {confirmation.appointment.department}
        Doctor: {confirmation.doctor.name}
        Date: {confirmation.appointment_date}
        Time: {confirmation.appointment_time}
        Phone: {confirmation.appointment.phone_number}
        
        Confirmed by: {request.user.full_name}
        """
        
        Notification.objects.create(
            patient=request.user,
            title=admin_notification_title,
            message=admin_notification_message,
            notification_type='appointment',
            related_id=confirmation.appointment.id
        )
        
        return Response({"message": "Appointment confirmed successfully."}, status=status.HTTP_201_CREATED)


# ✅ View Patient Appointment History
class PatientAppointmentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patient = request.user
        appointments = Appointment.objects.filter(patient=patient, is_confirmed=True)
        serializer = PatientAppointmentHistorySerializer(appointments, many=True)
        return Response(serializer.data)


# ✅ View Patient Upcoming Appointments
class PatientUpcomingAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from datetime import date
        patient = request.user
        
        # Get confirmed appointments with future dates
        upcoming_appointments = []
        
        # Get all confirmed appointments for this patient
        confirmed_appointments = Appointment.objects.filter(
            patient=patient, 
            is_confirmed=True
        ).prefetch_related('confirmation', 'confirmation__doctor')
        
        for appointment in confirmed_appointments:
            # Check if appointment has confirmation details
            if hasattr(appointment, 'confirmation') and appointment.confirmation:
                confirmation = appointment.confirmation
                if confirmation.appointment_date >= date.today():
                    upcoming_appointments.append({
                        'id': appointment.id,
                        'patient_name': appointment.full_name,
                        'department': appointment.department,
                        'doctor_name': confirmation.doctor.name,
                        'appointment_date': confirmation.appointment_date,
                        'appointment_time': confirmation.appointment_time,
                        'symptoms': appointment.symptoms,
                        'phone_number': appointment.phone_number,
                        'email': appointment.email,
                        'created_at': appointment.created_at
                    })
            else:
                # Handle appointments that are confirmed but missing confirmation details
                # Use appointment creation date as fallback
                appointment_date = appointment.created_at.date()
                if appointment_date >= date.today():
                    upcoming_appointments.append({
                        'id': appointment.id,
                        'patient_name': appointment.full_name,
                        'department': appointment.department,
                        'doctor_name': 'To be assigned',  # Default since no doctor assigned
                        'appointment_date': appointment_date,
                        'appointment_time': '09:00:00',  # Default time
                        'symptoms': appointment.symptoms,
                        'phone_number': appointment.phone_number,
                        'email': appointment.email,
                        'created_at': appointment.created_at,
                        'status': 'Confirmed (Pending Details)'
                    })
        
        # Sort by appointment date and time
        upcoming_appointments.sort(key=lambda x: (x['appointment_date'], x['appointment_time']))
        
        return Response({
            'upcoming_appointments': upcoming_appointments,
            'total_upcoming': len(upcoming_appointments)
        })


# ✅ Get Doctors by Department
class DoctorsByDepartmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        department = request.GET.get('department')
        if not department:
            return Response({"error": "Department parameter is required"}, status=400)
        
        doctors = Doctor.objects.filter(department=department, is_available=True)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)


# ✅ Reject/Cancel Appointment (Admin View)
class RejectAppointmentView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            reason = request.data.get('reason', 'No reason provided')
            
            # Create notification for patient
            from notification.models import Notification
            
            patient_notification_title = "Appointment Request Rejected"
            patient_notification_message = f"""
            Your appointment request has been rejected.
            
            Department: {appointment.department}
            Date Requested: {appointment.created_at.strftime('%Y-%m-%d')}
            Reason: {reason}
            
            Please contact us for more information or to schedule a new appointment.
            """
            
            Notification.objects.create(
                patient=appointment.patient,
                title=patient_notification_title,
                message=patient_notification_message,
                notification_type='appointment',
                related_id=appointment.id
            )
            
            # Create notification for admin
            admin_notification_title = f"Appointment Rejected - {appointment.full_name}"
            admin_notification_message = f"""
            Appointment rejected:
            
            Patient: {appointment.full_name}
            Department: {appointment.department}
            Phone: {appointment.phone_number}
            Reason: {reason}
            
            Rejected by: {request.user.full_name}
            """
            
            Notification.objects.create(
                patient=request.user,
                title=admin_notification_title,
                message=admin_notification_message,
                notification_type='appointment',
                related_id=appointment.id
            )
            
            # Delete the appointment
            appointment.delete()
            
            return Response({"message": "Appointment rejected successfully."}, status=status.HTTP_200_OK)
            
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
