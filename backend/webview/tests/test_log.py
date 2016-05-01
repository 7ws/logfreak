from unittest import mock

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse as r
import pytest

from backend.base.models import LogEntry
from backend.webview.views.log import UserLogEntriesView


class TestUserLogEntriesView:

    """Tests for backend.webview.views.log.UserLogEntriesView
    """

    def test_requesting_the_view_wont_crash(self, admin_client):
        """Check if the view is accessible
        """
        url = r('log:log')
        resp = admin_client.get(url)
        assert resp.status_code == 200

    @pytest.mark.django_db
    def test_make_sure_logs_are_filtered_by_user(self):
        """Make sure the log list view will query logs from logged user only
        """
        # Create users
        User = get_user_model()
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')

        # Create one log entry for each user
        log_entry = LogEntry.objects.create(user=user1)
        LogEntry.objects.create(user=user2)

        # Check view result
        view = UserLogEntriesView(request=mock.Mock(user=user1))
        queryset = view.get_queryset()
        assert list(queryset) == [log_entry]
