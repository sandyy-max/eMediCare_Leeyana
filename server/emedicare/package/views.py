# package/views.py
from rest_framework import generics, permissions, parsers
from rest_framework.response import Response
from rest_framework import status
from .models import HealthPackage, PackagePurchase
from .serializers import HealthPackageSerializer, PackagePurchaseSerializer
from notification.models import Notification

class PackageListView(generics.ListAPIView):
    queryset = HealthPackage.objects.all()
    serializer_class = HealthPackageSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to view packages


class PackagePurchaseView(generics.CreateAPIView):
    queryset = PackagePurchase.objects.all()
    serializer_class = PackagePurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require authentication
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def perform_create(self, serializer):
        print(f"Creating package purchase for user: {self.request.user}")
        print(f"Data received: {self.request.data}")
        print(f"Content-Type: {self.request.content_type}")
        
        # Use the authenticated user as the patient
        patient = self.request.user
        package_purchase = serializer.save(patient=patient)
        
        # Create notification for admin about the package booking
        admin_notification_title = f"New Package Booking - {package_purchase.package.name}"
        admin_notification_message = f"""
        Patient: {patient.full_name}
        Package: {package_purchase.package.name}
        Date: {package_purchase.selected_date}
        Price: NPR {package_purchase.package.price}
        Contact: {patient.phone_number}
        Email: {patient.email}
        
        Patient Details: {package_purchase.patient_details}
        """
        
        # Create admin notification (send to all admins)
        from userauth.models import User
        admin_users = User.objects.filter(role='admin')
        for admin_user in admin_users:
            Notification.objects.create(
                patient=admin_user,
                title=admin_notification_title,
                message=admin_notification_message,
                notification_type='package',
                related_id=package_purchase.id
            )
        
        # Create notification for patient
        patient_notification_title = f"Package Booking Confirmed - {package_purchase.package.name}"
        patient_notification_message = f"""
        Your {package_purchase.package.name} package has been booked successfully!
        
        Booking Details:
        - Package: {package_purchase.package.name}
        - Date: {package_purchase.selected_date}
        - Price: NPR {package_purchase.package.price}
        - Duration: {package_purchase.package.duration_days} days
        
        We will contact you shortly to confirm your appointment.
        """
        
        Notification.objects.create(
            patient=patient,
            title=patient_notification_title,
            message=patient_notification_message,
            notification_type='package',
            related_id=package_purchase.id
        )
        
        print(f"Package purchase created successfully for {patient.full_name}")

    def create(self, request, *args, **kwargs):
        print(f"=== CREATE METHOD CALLED ===")
        print(f"Request data: {request.data}")
        print(f"Request content type: {request.content_type}")
        print(f"Authenticated user: {request.user}")
        
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            print(f"Error in create: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            traceback.print_exc()
            raise


class PatientPurchaseListView(generics.ListAPIView):
    serializer_class = PackagePurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PackagePurchase.objects.filter(patient=self.request.user)


class AdminPurchaseListView(generics.ListAPIView):
    queryset = PackagePurchase.objects.all()
    serializer_class = PackagePurchaseSerializer
    permission_classes = [permissions.IsAdminUser]
