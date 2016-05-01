from django.conf.urls import url

from ..views import log


urlpatterns = [
    # Log entries list
    url(r'^log/$', log.UserLogEntriesView.as_view(), name='log'),

    # Log entry creation
    url(
        r'^log/create_(?P<type>{types})$'.format(
            types='|'.join(log.UserLogEntryCreate._form_class_map.keys())
        ),
        log.UserLogEntryCreate.as_view(),
        name='create_entry'),
]
