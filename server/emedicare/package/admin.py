# package/admin.py
from django.contrib import admin
from .models import HealthPackage, PackagePurchase

admin.site.register(HealthPackage)

@admin.register(PackagePurchase)
class PackagePurchaseAdmin(admin.ModelAdmin):
    list_display = ['patient', 'package', 'selected_date', 'valid_until', 'payment_status']
    search_fields = ['patient__full_name', 'package__name']
