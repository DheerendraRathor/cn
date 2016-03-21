from django.db import models

from organization.models.organization import FacultyInCharge
from organization.models.organization import StudentLeader
from organization.models.recipient import Recipient
from organization.models.utils import VerificationChoices


class AbstractVerificationModel(models.Model):
    verification_status = models.PositiveSmallIntegerField(choices=VerificationChoices.choices(),
                                                           default=VerificationChoices.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    citation = models.TextField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class StudentLeaderVerification(AbstractVerificationModel):
    recipient = models.OneToOneField(Recipient, related_name='student_leader_verification')
    verifier = models.ForeignKey(StudentLeader, related_name='verifications', null=True)

    def __str__(self):
        return str(self.recipient)


class FacultyVerification(AbstractVerificationModel):
    recipient = models.OneToOneField(Recipient, related_name='faculty_verification')
    verifier = models.ForeignKey(FacultyInCharge, related_name='verifications', null=True)

    def __str__(self):
        return str(self.recipient)
