from django.urls import path
from .views import UserProfileView, PasswordChangeView, MedicalInfoView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
    path('medical-info/', MedicalInfoView.as_view(), name='medical-info'),
] 