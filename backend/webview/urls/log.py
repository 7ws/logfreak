from django.conf.urls import url

from ..views import log


urlpatterns = [
    # Log entries list
    url(r'^log/$', log.UserLogEntriesView.as_view(), name='log'),

    # Log entry creation
    url(
        r'^log/create/$',
        log.UserLogEntryCreate.as_view(),
        name='create_entry'),
]
