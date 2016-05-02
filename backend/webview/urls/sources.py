from django.conf.urls import url

from ..views import sources


urlpatterns = [
    # Sources list
    url(
        r'^$',
        sources.UserSourcesListView.as_view(),
        name='list',
    ),
]
