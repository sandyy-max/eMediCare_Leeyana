# package/views.py
from rest_framework import generics, permissions
from .models import HealthPackage, PackagePurchase
from .serializers import HealthPackageSerializer, PackagePurchaseSerializer

class PackageListView(generics.ListAPIView):
    queryset = HealthPackage.objects.all()
    serializer_class = HealthPackageSerializer
    permission_classes = [permissions.IsAuthenticated]


class PackagePurchaseView(generics.CreateAPIView):
    queryset = PackagePurchase.objects.all()
    serializer_class = PackagePurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)


class PatientPurchaseListView(generics.ListAPIView):
    serializer_class = PackagePurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PackagePurchase.objects.filter(patient=self.request.user)


class AdminPurchaseListView(generics.ListAPIView):
    queryset = PackagePurchase.objects.all()
    serializer_class = PackagePurchaseSerializer
    permission_classes = [permissions.IsAdminUser]
