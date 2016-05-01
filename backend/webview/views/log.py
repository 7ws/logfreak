from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext as _
from django.views import generic

from backend.base.models import LogEntry


class UserLogEntriesView(LoginRequiredMixin, generic.ListView):

    """List all log entries of an user
    """

    page_title = _('My log')
    template_name = 'log/log_list.jade'

    def get_queryset(self):
        return LogEntry.objects.filter(user=self.request.user)
