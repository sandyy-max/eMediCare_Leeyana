from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer, NotificationCreateSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            # Admin can see all notifications
            return Notification.objects.all()
        else:
            # Patients can only see their own notifications
            return Notification.objects.filter(patient=user)

class NotificationDetailView(generics.RetrieveAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Notification.objects.all()
        else:
            return Notification.objects.filter(patient=user)

class MarkNotificationAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, notification_id):
        try:
            user = request.user
            if user.role == 'admin':
                notification = Notification.objects.get(id=notification_id)
            else:
                notification = Notification.objects.get(id=notification_id, patient=user)
            
            notification.is_read = True
            notification.save()
            
            return Response({
                "message": "Notification marked as read",
                "notification_id": notification_id
            }, status=status.HTTP_200_OK)
            
        except Notification.DoesNotExist:
            return Response({
                "error": "Notification not found"
            }, status=status.HTTP_404_NOT_FOUND)

class UnreadCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        if user.role == 'admin':
            count = Notification.objects.filter(is_read=False).count()
        else:
            count = Notification.objects.filter(patient=user, is_read=False).count()
        
        return Response({
            "count": count
        }, status=status.HTTP_200_OK)

class CreateNotificationView(generics.CreateAPIView):
    serializer_class = NotificationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Only admin can create notifications
        if self.request.user.role != 'admin':
            raise permissions.PermissionDenied("Only administrators can create notifications")
        serializer.save()

