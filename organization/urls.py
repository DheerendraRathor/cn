from django.conf.urls import url
from .views import ShowAwardsHistory, AddNewObjectView

urlpatterns = [
    url(r'^new/$', AddNewObjectView.as_view(), name='new'),
    url(r'^history/$', ShowAwardsHistory.as_view(), name='history'),
]
