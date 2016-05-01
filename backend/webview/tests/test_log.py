from unittest import mock

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse as r
import pytest

from backend.base import models as base_models
from backend.sms_logger import models as sms_models
from backend.webview.forms import log as log_forms
from backend.webview.views import log as log_views


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
        log_entry = base_models.LogEntry.objects.create(user=user1)
        base_models.LogEntry.objects.create(user=user2)

        # Check view result
        view = log_views.UserLogEntriesView(request=mock.Mock(user=user1))
        queryset = view.get_queryset()
        assert list(queryset) == [log_entry]


class TestUserLogEntryCreate:

    """Tests for backend.webview.views.log.UserLogEntryCreate
    """

    def test_view_retrieves_right_form_class_from_sms_input(self, admin_user):
        """Check if `SMSEntryForm` is selected when view receives kwarg
        """
        view = log_views.UserLogEntryCreate(
            request=mock.Mock(user=admin_user),
            kwargs={'type': 'sms'},
        )
        form_class = view.get_form_class()
        assert form_class == log_forms.SMSEntryForm

    def test_user_is_able_to_create_sms_entry(self, admin_user, admin_client):
        """Check if the user is able to create a SMS entry through the view
        """
        # Create some required objects
        contact = base_models.Contact.objects.create(
            _type=base_models.Contact.TYPE_PERSON,
            name='John Doe',
            user=admin_user,
        )
        contact_phone = contact.contactphone_set.create(
            user=admin_user,
            msisdn='+5511912345678',
        )

        # Post data to URL
        url = r('log:create_entry', kwargs={'type': 'sms'})
        post_data = {
            'contact_phone': contact_phone.pk,
            'datetime': '2000-01-01 00:00:00',
            'text': 'Hello world',
        }
        admin_client.post(url, post_data)

        # Check created object
        assert sms_models.SMSEntry.objects.exists()
