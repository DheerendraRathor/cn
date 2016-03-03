from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from organization.models import StudentLeaderVerification


class ValidateStudentVerification(TemplateView):

    def get(self, request, *args, **kwargs):
        recipient_id = kwargs.pop('recipient_id', None)  # type: str
        verification_key = kwargs.pop('key', None)  # type: str

        if (not recipient_id or not recipient_id.isdigit()) or not verification_key:
            raise Http404

        verification_obj = get_object_or_404(
            StudentLeaderVerification.objects.select_related('recipient__user',
                                                             'recipient__organization_object__organization'),
            recipient_id=int(recipient_id),
            verification_key=verification_key
        )
        #TODO: Render template here
