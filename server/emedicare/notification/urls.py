from django.urls import path
from .views import (
    NotificationListView, 
    NotificationDetailView, 
    MarkNotificationAsReadView,
    UnreadCountView,
    CreateNotificationView
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('<int:notification_id>/mark-read/', MarkNotificationAsReadView.as_view(), name='mark-notification-read'),
    path('unread-count/', UnreadCountView.as_view(), name='unread-count'),
    path('create/', CreateNotificationView.as_view(), name='create-notification'),
]