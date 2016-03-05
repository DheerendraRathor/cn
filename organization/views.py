from typing import Tuple

from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView

from organization.forms import VerificationForm
from organization.models import StudentLeaderVerification, FacultyVerification, VerificationChoices


class ValidateStudentVerification(TemplateView):

    template_name = 'validation/student_validation.html'

    def get_verification_object(self, recipient_id: int, verification_key: str) -> StudentLeaderVerification:
        verification_obj = get_object_or_404(  # type: StudentLeaderVerification
            StudentLeaderVerification.objects.select_related(
                'recipient__user',
                'recipient__organization_object__organization',
                'verifier'
            ).filter(verification_status=VerificationChoices.PENDING),
            recipient_id=recipient_id,
            verification_key=verification_key
        )
        return verification_obj

    def validate_request(self, request, *args, **kwargs) -> Tuple[int, str]:
        recipient_id = kwargs.pop('recipient_id', None)  # type: str
        verification_key = kwargs.pop('key', None)  # type: str

        if (not recipient_id or not recipient_id.isdigit()) or not verification_key:
            raise Http404

        return int(recipient_id), verification_key

    def update_context(self, verification_obj: StudentLeaderVerification, kwargs: dict) -> dict:
        kwargs['organization'] = verification_obj.recipient.organization_object.organization
        kwargs['organization_object'] = verification_obj.recipient.organization_object
        kwargs['recipient'] = verification_obj.recipient
        kwargs['verifier'] = verification_obj.verifier
        kwargs['verification_form'] = VerificationForm()
        kwargs['verification_choices'] = VerificationChoices
        return kwargs

    def get(self, request, *args, **kwargs):
        recipient_id, verification_key = self.validate_request(request, *args, **kwargs)

        verification_obj = self.get_verification_object(recipient_id, verification_key)

        kwargs = self.update_context(verification_obj, kwargs)

        return super().get(request, *args, **kwargs)

    def post_post(self, verification_obj: StudentLeaderVerification):
        """
        Method to call post post operation. It will create faculty verification object
        """
        faculty_verification_obj = FacultyVerification(
            recipient=verification_obj.recipient,
            verifier=verification_obj.recipient.organization_object.organization.faculty_incharge,
        )
        # TODO: Send Mail
        faculty_verification_obj.save()

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        recipient_id, verification_key = self.validate_request(request, *args, **kwargs)

        verification_obj = self.get_verification_object(recipient_id, verification_key)

        verification_form = VerificationForm(data=request.POST)
        if verification_form.is_valid():
            verification_obj.verification_status = verification_form.cleaned_data.get(
                'verification_status', VerificationChoices.REJECTED)
            verification_obj.citation = verification_form.cleaned_data.get('citation')
            verification_obj.rejection_reason = verification_form.cleaned_data.get('rejection_reason')
            verification_obj.verified_at = timezone.now()
            verification_obj.save()
            self.post_post(verification_obj)
            return HttpResponse('<h1>Thanks for Verification. You may close the window now')
        else:
            kwargs = self.update_context(verification_obj, kwargs)
            kwargs['verification_form'] = verification_form

            return super().get(request, *args, **kwargs)


class ValidateFacultyVerification(ValidateStudentVerification):

    template_name = 'validation/faculty_validation.html'

    def get_verification_object(self, recipient_id: int, verification_key: str) -> FacultyVerification:
        verification_obj = get_object_or_404(  # type: FacultyVerification
            FacultyVerification.objects.select_related(
                'recipient__user',
                'recipient__organization_object__organization',
                'recipient__student_leader_verification__verifier',
                'verifier',
            ).filter(
                verification_status=VerificationChoices.PENDING,
                recipient__student_leader_verification__verification_status=VerificationChoices.VERIFIED,
            ),
            recipient_id=recipient_id,
            verification_key=verification_key
        )
        return verification_obj

    def update_context(self, verification_obj: FacultyVerification, kwargs: dict) -> dict:
        kwargs = super().update_context(verification_obj, kwargs)
        kwargs['student_leader_verification'] = verification_obj.recipient.student_leader_verification
        kwargs['student_verifier'] = verification_obj.recipient.student_leader_verification.verifier
        kwargs['verifier'] = verification_obj.verifier
        return kwargs

    def post_post(self, verification_object: FacultyVerification):
        pass
