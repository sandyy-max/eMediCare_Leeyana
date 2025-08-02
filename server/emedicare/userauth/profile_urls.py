from django.urls import path
from .views import UserProfileView, PasswordChangeView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
] 