from rest_framework import generics, permissions, status, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.utils import timezone
from .models import Medicine, Prescription, MedicineRequest
from .serializer import MedicineSerializer, PrescriptionSerializer, MedicineRequestSerializer, MedicineRequestAdminSerializer

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
        medicine_request = serializer.save(patient=self.request.user)
        
        # Create notification for admin
        from notification.models import Notification
        
        admin_notification_title = f"New Medicine Request - {medicine_request.medicine_name}"
        admin_notification_message = f"""
        Patient: {medicine_request.patient_name}
        Medicine: {medicine_request.medicine_name}
        Dosage: {medicine_request.dosage}
        Quantity: {medicine_request.quantity}
        Urgency: {medicine_request.urgency}
        Contact: {medicine_request.contact_number}
        
        Please review and process this request.
        """
        
        # Send notification to all admin users
        from userauth.models import User
        admin_users = User.objects.filter(role='admin')
        for admin_user in admin_users:
            Notification.objects.create(
                patient=admin_user,
                title=admin_notification_title,
                message=admin_notification_message,
                notification_type='medicine',
                related_id=medicine_request.id
            )
        
        # Create notification for patient
        patient_notification_title = "Medicine Request Submitted"
        patient_notification_message = f"""
        Your medicine request for {medicine_request.medicine_name} has been submitted successfully.
        
        Request Details:
        - Medicine: {medicine_request.medicine_name}
        - Dosage: {medicine_request.dosage}
        - Quantity: {medicine_request.quantity}
        - Urgency: {medicine_request.urgency}
        
        We will review your request and contact you shortly.
        """
        
        Notification.objects.create(
            patient=self.request.user,
            title=patient_notification_title,
            message=patient_notification_message,
            notification_type='medicine',
            related_id=medicine_request.id
        )
    
    def create(self, request, *args, **kwargs):
        print(f"Medicine request received: {request.data}")
        print(f"Content-Type: {request.content_type}")
        print(f"Request method: {request.method}")
        print(f"Request user: {request.user}")
        print(f"Request files: {request.FILES}")
        
        try:
            result = super().create(request, *args, **kwargs)
            print(f"Medicine request created successfully: {result.data}")
            return result
        except Exception as e:
            print(f"Error creating medicine request: {str(e)}")
            raise

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


# Admin Management Views
class AdminMedicineRequestListView(generics.ListAPIView):
    serializer_class = MedicineRequestAdminSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        status_filter = self.request.query_params.get('status', None)
        queryset = MedicineRequest.objects.all()
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-requested_at')


class AdminMedicineRequestDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = MedicineRequestAdminSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return MedicineRequest.objects.all()
    
    def update(self, request, *args, **kwargs):
        medicine_request = self.get_object()
        old_status = medicine_request.status
        new_status = request.data.get('status', old_status)
        admin_comments = request.data.get('admin_comments', '')
        
        # Update the request
        medicine_request.status = new_status
        medicine_request.admin_comments = admin_comments
        medicine_request.processed_by = request.user
        medicine_request.processed_at = timezone.now()
        medicine_request.save()
        
        # Create notification for patient
        from notification.models import Notification
        
        if new_status != old_status:
            if new_status == 'approved':
                notification_title = "Medicine Request Approved"
                notification_message = f"""
                Your medicine request for {medicine_request.medicine_name} has been approved!
                
                Request Details:
                - Medicine: {medicine_request.medicine_name}
                - Dosage: {medicine_request.dosage}
                - Quantity: {medicine_request.quantity}
                
                Admin Comments: {admin_comments}
                
                Please collect your medicine from the pharmacy.
                """
            elif new_status == 'denied':
                notification_title = "Medicine Request Denied"
                notification_message = f"""
                Your medicine request for {medicine_request.medicine_name} has been denied.
                
                Request Details:
                - Medicine: {medicine_request.medicine_name}
                - Dosage: {medicine_request.dosage}
                - Quantity: {medicine_request.quantity}
                
                Admin Comments: {admin_comments}
                
                Please contact us for more information.
                """
            elif new_status == 'in_progress':
                notification_title = "Medicine Request In Progress"
                notification_message = f"""
                Your medicine request for {medicine_request.medicine_name} is being processed.
                
                Request Details:
                - Medicine: {medicine_request.medicine_name}
                - Dosage: {medicine_request.dosage}
                - Quantity: {medicine_request.quantity}
                
                Admin Comments: {admin_comments}
                
                We will update you once the processing is complete.
                """
            elif new_status == 'completed':
                notification_title = "Medicine Request Completed"
                notification_message = f"""
                Your medicine request for {medicine_request.medicine_name} has been completed!
                
                Request Details:
                - Medicine: {medicine_request.medicine_name}
                - Dosage: {medicine_request.dosage}
                - Quantity: {medicine_request.quantity}
                
                Admin Comments: {admin_comments}
                
                Your medicine is ready for pickup.
                """
            else:
                notification_title = "Medicine Request Updated"
                notification_message = f"""
                Your medicine request for {medicine_request.medicine_name} has been updated.
                
                New Status: {new_status}
                Admin Comments: {admin_comments}
                """
            
            Notification.objects.create(
                patient=medicine_request.patient,
                title=notification_title,
                message=notification_message,
                notification_type='medicine',
                related_id=medicine_request.id
            )
        
        return Response({
            "message": f"Medicine request {new_status} successfully",
            "status": new_status,
            "admin_comments": admin_comments
        })


class MedicineRequestStatsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        total_requests = MedicineRequest.objects.count()
        pending_requests = MedicineRequest.objects.filter(status='pending').count()
        in_progress_requests = MedicineRequest.objects.filter(status='in_progress').count()
        approved_requests = MedicineRequest.objects.filter(status='approved').count()
        denied_requests = MedicineRequest.objects.filter(status='denied').count()
        completed_requests = MedicineRequest.objects.filter(status='completed').count()
        
        return Response({
            'total_requests': total_requests,
            'pending_requests': pending_requests,
            'in_progress_requests': in_progress_requests,
            'approved_requests': approved_requests,
            'denied_requests': denied_requests,
            'completed_requests': completed_requests
        })
