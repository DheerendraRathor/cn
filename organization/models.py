import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.functional import cached_property


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

    def __str__(self):
        return "{} - {}".format(self.organization_object, self.user.username)

    class Meta:
        unique_together = ('user', 'organization_object')


class StudentLeaderVerification(models.Model):
    recipient = models.OneToOneField(Recipient, related_name='student_leader_verification')
    verification_key = models.UUIDField(default=uuid.uuid4)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True)


class FacultyVerification(models.Model):
    recipient = models.OneToOneField(Recipient, related_name='faculty_verification')
    verification_key = models.UUIDField(default=uuid.uuid4)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True)