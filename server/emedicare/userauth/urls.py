# accounts/urls.py

from django.urls import path
from .views import RegisterView, LoginView, UserProfileView
urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('token/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
