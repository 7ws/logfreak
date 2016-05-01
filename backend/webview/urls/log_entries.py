from django.conf.urls import url

from ..views import log_entries


urlpatterns = [
    # Log entries list
    url(r'^log/$', log_entries.UserLogEntriesView.as_view(), name='log'),
]
