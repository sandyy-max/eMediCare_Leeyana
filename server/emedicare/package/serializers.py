# package/serializers.py
from rest_framework import serializers
from .models import HealthPackage, PackagePurchase

class HealthPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthPackage
        fields = '__all__'


class PackagePurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackagePurchase
        fields = '__all__'
        read_only_fields = ['purchased_at', 'payment_status', 'valid_until']
