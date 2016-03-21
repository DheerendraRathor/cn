from django.contrib import admin
from .models import (Organization, OrganizationObject, Recipient, StudentLeaderVerification, FacultyVerification,
                     StudentLeader, FacultyInCharge)


class RecipientInline(admin.TabularInline):
    model = Recipient
    extra = 0
    show_change_link = True
    show_full_result_count = True


class OrganizationObjectAdmin(admin.ModelAdmin):
    inlines = [RecipientInline]
    list_filter = ['organization', 'object_type']


class OrganizationObjectInline(admin.TabularInline):
    model = OrganizationObject
    show_change_link = True
    show_full_result_count = True
    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    inlines = [OrganizationObjectInline]
    search_fields = ['name', 'student_leader_username', 'faculty_in_charge_username']


class StudentLeaderVerificationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'verification_status']
    list_filter = ['verification_status']


class FacultyVerificationAdmin(admin.ModelAdmin):
    pass


class RecipientAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization_object', 'student_leader_verification_status',
                    'faculty_incharge_verification_status']
    list_filter = ['organization_object__organization']


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationObject, OrganizationObjectAdmin)
admin.site.register(Recipient, RecipientAdmin)
admin.site.register(StudentLeaderVerification, StudentLeaderVerificationAdmin)
admin.site.register(FacultyVerification, FacultyVerificationAdmin)
admin.site.register(StudentLeader)
admin.site.register(FacultyInCharge)
