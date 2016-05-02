from unittest import mock

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse as r
import pytest

from backend.base import models as base_models
from backend.webview.views import sources as sources_views


class TestUserSourcesListView:

    """Tests for `backend.webview.views.sources.UserSourcesListView`
    """

    def test_requesting_the_view_wont_crash(self, admin_client):
        """Check if the view is accessible
        """
        url = r('sources:list')
        resp = admin_client.get(url)
        assert resp.status_code == 200

    @pytest.mark.django_db
    def test_make_sure_objects_are_filtered_by_user(self):
        """Make sure the list view queries sources from logged user only
        """
        # Create users
        User = get_user_model()
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')

        # Create one log entry for each user
        source = base_models.Source.objects.create(user=user1)
        base_models.Source.objects.create(user=user2)

        # Check view result
        view = sources_views.UserSourcesListView(request=mock.Mock(user=user1))
        queryset = view.get_queryset()
        assert list(queryset) == [source]
