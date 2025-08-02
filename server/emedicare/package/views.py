# package/views.py
from rest_framework import generics, permissions, parsers
from .models import HealthPackage, PackagePurchase
from .serializers import HealthPackageSerializer, PackagePurchaseSerializer

class PackageListView(generics.ListAPIView):
    queryset = HealthPackage.objects.all()
    serializer_class = HealthPackageSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to view packages


class PackagePurchaseView(generics.CreateAPIView):
    queryset = PackagePurchase.objects.all()
    serializer_class = PackagePurchaseSerializer
    permission_classes = [permissions.AllowAny]  # Temporarily allow all for testing
    parser_classes = [parsers.JSONParser]

    def perform_create(self, serializer):
        print(f"Creating package purchase for user: {self.request.user}")
        print(f"Data received: {self.request.data}")
        print(f"Content-Type: {self.request.content_type}")
        # Create a dummy user for now
        from userauth.models import User
        user = User.objects.first()
        serializer.save(patient=user)
        print(f"Package purchase created successfully")

    def create(self, request, *args, **kwargs):
        print(f"=== CREATE METHOD CALLED ===")
        print(f"Request data: {request.data}")
        print(f"Request content type: {request.content_type}")
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
