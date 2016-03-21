from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from organization.models import Recipient


class ShowAwardsHistory(LoginRequiredMixin, TemplateView):

    template_name = 'student/history.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        recipients = Recipient.objects.all().filter(
            user=user).select_related('organization_object__organization',
                                      'student_leader_verification',
                                      'faculty_verification')

        kwargs['recipients'] = recipients
        return super().get(request, *args, **kwargs)
