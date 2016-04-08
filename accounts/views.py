from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import View

from accounts.models import NotificationMail


class LoginByEmailView(View):

    def get(self, request, key):
        now = timezone.now()
        notification_mail = get_object_or_404(  # type: NotificationMail
            NotificationMail.objects.filter(expire_on__gt=now),
            key=key,
        )

        user = notification_mail.user
        login(request, user)
        return redirect('index')
