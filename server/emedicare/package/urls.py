# package/urls.py
from django.urls import path
from .views import (
    PackageListView,
    PackagePurchaseView,
    PatientPurchaseListView,
    AdminPurchaseListView
)

urlpatterns = [
    path('', PackageListView.as_view(), name='package-list'),
    path('purchase/', PackagePurchaseView.as_view(), name='package-purchase'),
    path('my-purchases/', PatientPurchaseListView.as_view(), name='my-purchases'),
    path('admin-purchases/', AdminPurchaseListView.as_view(), name='admin-purchases'),
]
