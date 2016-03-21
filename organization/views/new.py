from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum, Case, When, IntegerField, F
from django.shortcuts import render
from django.views.generic import TemplateView

from organization.models import Organization, OrganizationObject, Recipient, VerificationChoices, \
    StudentLeaderVerification


class AddNewObjectView(LoginRequiredMixin, TemplateView):
    template_name = 'student/new.html'

    def get_base_organization_object_query(self):
        return OrganizationObject.objects.exclude(
                recipients__user=self.request.user,  # user already applied for this post
            ).annotate(
                recipients_count=Sum(
                    Case(
                        When(
                            recipients__faculty_verification__verification_status=VerificationChoices.VERIFIED,
                            then=1
                        ),
                        default=0,
                        output_field=IntegerField(),
                    )
                )
            ).exclude(
                recipients_count__gte=F('max_recipients'),
            )

    def get(self, request, *args, **kwargs):

        organization = request.GET.get('org', None)

        organizations = Organization.objects.all()

        if organization is not None:
            try:
                organization = int(organization)
            except ValueError:
                organization = None

        if organization:
            objects = self.get_base_organization_object_query().filter(
                organization_id=organization,
            )

        else:
            objects = None

        kwargs['organization_asked'] = organization
        kwargs['organizations'] = organizations
        kwargs['objects'] = objects

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        organization_object = request.POST.get('object', None)
        if organization_object:
            try:
                organization_object = int(organization_object)
            except ValueError:
                organization_object = None

        if organization_object:
            organization_object = self.get_base_organization_object_query().filter(
                id=organization_object,
            ).first()

        if organization_object:
            with transaction.atomic():
                recipient = Recipient(
                    user=request.user,
                    organization_object=organization_object,
                    self_appraisal=request.POST.get('self_appraisal'),

                )
                recipient.save()
                student_leader_verification = StudentLeaderVerification(
                    recipient=recipient,
                    verifier=organization_object.organization.student_leader,
                )
                student_leader_verification.save()

                return render(request, 'student/success.html', {'message': 'Request created'})

        return self.get(request, *args, **kwargs)