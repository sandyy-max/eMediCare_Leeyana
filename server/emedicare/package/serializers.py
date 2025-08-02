# package/serializers.py
from rest_framework import serializers
from .models import HealthPackage, PackagePurchase

class HealthPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthPackage
        fields = '__all__'


class PackagePurchaseSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(write_only=True, required=False)
    patient_details = serializers.JSONField(write_only=True, required=False)
    
    class Meta:
        model = PackagePurchase
        fields = '__all__'
        read_only_fields = ['purchased_at', 'payment_status', 'valid_until']
    
    def get_fields(self):
        fields = super().get_fields()
        # Make patient and package optional for write operations
        if self.context.get('request') and self.context['request'].method == 'POST':
            fields['patient'].required = False
            fields['package'].required = False
        return fields
    
    def validate(self, data):
        print(f"=== VALIDATE METHOD ===")
        print(f"Data to validate: {data}")
        return data
    
    def create(self, validated_data):
        print(f"=== SERIALIZER CREATE METHOD ===")
        print(f"Validated data: {validated_data}")
        
        package_name = validated_data.pop('package_name', None)
        patient_details = validated_data.pop('patient_details', {})
        
        print(f"Package name: {package_name}")
        print(f"Patient details: {patient_details}")
        
        # Get or create the package
        if package_name:
            package, created = HealthPackage.objects.get_or_create(
                name=package_name,
                defaults={
                    'description': f'Health package: {package_name}',
                    'price': 0.00
                }
            )
            validated_data['package'] = package
            print(f"Package: {package}")
        
        # Store patient details
        validated_data['patient_details'] = patient_details
        
        # Ensure selected_date is properly set
        if 'selected_date' not in validated_data:
            from datetime import date
            validated_data['selected_date'] = date.today()
        
        print(f"Final validated data: {validated_data}")
        return super().create(validated_data)
