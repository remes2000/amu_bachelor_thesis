from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import generic
from amu_bachelor_thesis_app.models import Notification


@method_decorator(login_required, name='dispatch')
class NotificationsView(generic.ListView):
    model = Notification
    template_name = 'amu_bachelor_thesis_app/notification/notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        notifications = Notification.objects.filter(recipient=self.request.user, is_seen=False).order_by('-date')
        for notification in notifications:
            notification.is_seen = True
            notification.save()
        return notifications


@method_decorator(login_required, name='dispatch')
class NotificationsHistoryView(generic.ListView):
    model = Notification
    template_name = 'amu_bachelor_thesis_app/notification/notifications-history.html'
    context_object_name = 'notifications'
    paginate_by = 15

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user, is_seen=True).order_by('-date')


@login_required
def notifications_get_counter(request):
    number_of_unread_notifications = Notification.objects.filter(recipient=request.user, is_seen=False).count()
    return JsonResponse({"unread_notifications": number_of_unread_notifications}, status=200)
