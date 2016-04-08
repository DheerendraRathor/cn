import uuid
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models


class NotificationMail(models.Model):
    user = models.ForeignKey(User)
    key = models.UUIDField(default=uuid.uuid4)
    created_on = models.DateTimeField(auto_now_add=True)
    expire_on = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.expire_on = self.created_on + timedelta(days=1)
        return super().save(*args, **kwargs)
