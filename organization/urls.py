from django.conf.urls import url
from .views import ValidateStudentVerification


urlpatterns = [
    url(r'^student_validation/(?P<recipient_id>\d+)/(?P<key>[0-9A-Za-z]+)/$', ValidateStudentVerification.as_view(), name='student_validation'),
    url(r'^faculty_validation/(?P<recipient_id>\d+)/(?P<key>[0-9A-Za-z]+)/$', None, name='faculty_validation'),
]
