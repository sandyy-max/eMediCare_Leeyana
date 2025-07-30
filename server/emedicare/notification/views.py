from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer

