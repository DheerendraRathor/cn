

from django.contrib.auth.models import User
from django.db import models

from organization.models.utils import OrganizationObjectType, MAX_RECIPIENTS


class StudentLeader(models.Model):
    user = models.ForeignKey(User, related_name='student_leader')
    designation = models.CharField(max_length=128)

    def __str__(self):
        return "{}, {}".format(self.user.get_full_name(), self.designation)


class FacultyInCharge(models.Model):
    user = models.ForeignKey(User, related_name='faculty_in_charge')
    designation = models.CharField(max_length=128)

    def __str__(self):
        return "{name}, {designation}".format(name=self.user.get_full_name(), designation=self.designation)


class Organization(models.Model):
    name = models.CharField(max_length=64)
    student_leader = models.ForeignKey(StudentLeader, related_name='organizations', null=True)
    faculty_incharge = models.ForeignKey(FacultyInCharge, related_name='organizations', null=True)

    def __str__(self):
        return self.name


class OrganizationObject(models.Model):
    name = models.CharField(max_length=64, help_text='Name of post')
    organization = models.ForeignKey(Organization, related_name='posts_and_rewards')
    object_type = models.PositiveSmallIntegerField(choices=OrganizationObjectType.choices(),
                                                   default=OrganizationObjectType.POST)
    max_recipients = models.PositiveIntegerField(default=MAX_RECIPIENTS)

    def __str__(self):
        return "{} - {}".format(self.organization.name, self.name)

    class Meta:
        verbose_name = 'Posts and Awards'
        verbose_name_plural = 'Posts and Awards'
        unique_together = ('name', 'organization')
