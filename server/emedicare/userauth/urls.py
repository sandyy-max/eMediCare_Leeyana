# accounts/urls.py

from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, PasswordChangeView, MedicalInfoView
urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('token/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
    path('medical-info/', MedicalInfoView.as_view(), name='medical-info'),
]
