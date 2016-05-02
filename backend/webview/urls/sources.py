from django.conf.urls import url

from ..views import sources
from backend.base.models import Source


urlpatterns = [
    # Sources list
    url(
        r'^$',
        sources.UserSourcesListView.as_view(),
        name='list',
    ),

    # Source creation (provider selection)
    url(
        r'^create$',
        sources.UserSourcePreCreateView.as_view(),
        name='create',
    ),

    # Source creation
    url(
        r'^create/(?P<name>{names})$'.format(
            names='|'.join(cls._name for cls in Source.__subclasses__()),
        ),
        sources.UserSourceCreateView.as_view(),
        name='create_for',
    ),

    # Manual source sync
    url(
        r'sync/(?P<pk>\d+)$',
        sources.ManualSourceSyncView.as_view(),
        name='sync',
    ),
]
