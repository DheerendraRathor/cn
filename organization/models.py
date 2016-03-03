import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils.functional import cached_property


class VerificationChoices(object):
    PENDING = 0
    VERIFIED = 1
    REJECTED = 2

    @classmethod
    def choices(cls):
        return [
            (cls.PENDING, 'Pending'),
            (cls.VERIFIED, 'Verified'),
            (cls.REJECTED, 'Rejected'),
        ]

    @classmethod
    def to_dict(cls):
        return {
            cls.PENDING, 'Pending',
            cls.VERIFIED, 'Verified',
            cls.REJECTED, 'Rejected',
        }


class Organization(models.Model):
    name = models.CharField(max_length=64)
    student_leader_username = models.CharField(max_length=64)
    faculty_in_charge_username = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class OrganizationObject(models.Model):
    name = models.CharField(max_length=64, help_text='Name of post')
    organization = models.ForeignKey(Organization, related_name='posts_and_rewards')
    is_post = models.BooleanField(default=False)
    max_recipients = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.organization.name, self.name)

    class Meta:
        verbose_name = 'Posts and Awards'
        verbose_name_plural = 'Posts and Awards'
        unique_together = ('name', 'organization')


class Recipient(models.Model):
    user = models.ForeignKey(User)
    organization_object = models.ForeignKey(OrganizationObject, related_name='recipients')
    requested_at = models.DateTimeField(auto_now_add=True)

    @cached_property
    def is_verified_by_student_leader(self) -> bool:
        try:
            return self.student_leader_verification.is_verified
        except ObjectDoesNotExist:
            return False

    @cached_property
    def is_verified_by_faculty_incharge(self) -> bool:
        try:
            return self.faculty_verification.is_verified
        except ObjectDoesNotExist:
            return False

    is_verified_by_student_leader.short_description = 'Verified by Student Leader'
    is_verified_by_faculty_incharge.short_description = 'Verified by faculty incharge'

    def clean(self):
        if self.pk is None:
            if self.organization_object.max_recipients is None:
                if self.organization_object.recipients.filter(
                    student_leader_verification__verification_status=VerificationChoices.VERIFIED,
                    faculty_verification__verification_status=VerificationChoices.VERIFIED,
                ).count() >= self.organization_object.max_recipients:
                    raise ValidationError('This position has already received enough recipients')

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.organization_object.recipients.count() >= self.organization_object.max_recipients:
                return False
        return super().save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.organization_object, self.user.username)

    class Meta:
        unique_together = ('user', 'organization_object')


class StudentLeaderVerification(models.Model):
    recipient = models.OneToOneField(Recipient, related_name='student_leader_verification')
    verification_key = models.UUIDField(default=uuid.uuid4)
    verification_status = models.PositiveSmallIntegerField(choices=VerificationChoices.choices(),
                                                           default=VerificationChoices.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True)
    citation = models.TextField(null=True, blank=True)


class FacultyVerification(models.Model):
    recipient = models.OneToOneField(Recipient, related_name='faculty_verification')
    verification_key = models.UUIDField(default=uuid.uuid4)
    verification_status = models.PositiveSmallIntegerField(choices=VerificationChoices.choices(),
                                                           default=VerificationChoices.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True)
    citation = models.TextField(null=True, blank=True)
