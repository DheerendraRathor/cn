from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils.functional import cached_property

from organization.models.organization import OrganizationObject
from organization.models.utils import VerificationChoices


class Recipient(models.Model):
    user = models.ForeignKey(User)
    organization_object = models.ForeignKey(OrganizationObject, related_name='recipients')
    self_appraisal = models.TextField(blank=True, null=True)
    is_self_appraisal_public = models.BooleanField(default=True)
    requested_at = models.DateTimeField(auto_now_add=True)

    @cached_property
    def student_leader_verification_status(self) -> VerificationChoices:
        try:
            return self.student_leader_verification.verification_status
        except ObjectDoesNotExist:
            return VerificationChoices.PENDING

    @cached_property
    def faculty_incharge_verification_status(self) -> VerificationChoices:
        try:
            return self.faculty_verification.verification_status
        except ObjectDoesNotExist:
            return VerificationChoices.PENDING

    student_leader_verification_status.short_description = 'Verified by Student Leader'
    faculty_incharge_verification_status.short_description = 'Verified by faculty incharge'

    @cached_property
    def render_student_leader_verification(self) -> str:
        return VerificationChoices.get_glyphicon_html(self.student_leader_verification_status)

    @cached_property
    def render_faculty_verification(self) -> str:
        return VerificationChoices.get_glyphicon_html(self.faculty_incharge_verification_status)

    def clean(self):
        if self.pk is None:
            if self.organization_object.max_recipients is None:
                if self.organization_object.recipients.filter(
                    student_leader_verification__verification_status=VerificationChoices.VERIFIED,
                    faculty_verification__verification_status=VerificationChoices.VERIFIED,
                ).count() >= self.organization_object.max_recipients:
                    raise ValidationError('This position has already received enough recipients')

    def __str__(self):
        return "{} - {}".format(self.organization_object, self.user.username)

    class Meta:
        unique_together = ('user', 'organization_object')
        ordering = ['-requested_at']
