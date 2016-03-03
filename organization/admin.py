from django.contrib import admin
from .models import Organization, OrganizationObject, Recipient, StudentLeaderVerification, FacultyVerification


class RecipientInline(admin.TabularInline):
    model = Recipient
    extra = 0
    show_change_link = True
    show_full_result_count = True


class OrganizationObjectAdmin(admin.ModelAdmin):
    inlines = [RecipientInline]
    list_filter = ['organization', 'is_post']


class OrganizationObjectInline(admin.TabularInline):
    model = OrganizationObject
    show_change_link = True
    show_full_result_count = True
    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    inlines = [OrganizationObjectInline]
    search_fields = ['name', 'student_leader_username', 'faculty_in_charge_username']


class StudentLeaderVerificationInline(admin.TabularInline):
    model = StudentLeaderVerification


class FacultyVerificationInline(admin.TabularInline):
    model = FacultyVerification


class RecipientAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified_by_student_leader', 'is_verified_by_faculty_incharge']
    list_filter = ['organization_object__organization']
    inlines = [StudentLeaderVerificationInline, FacultyVerificationInline]


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationObject, OrganizationObjectAdmin)
admin.site.register(Recipient, RecipientAdmin)
