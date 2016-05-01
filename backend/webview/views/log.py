from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse as r
from django.http import HttpResponseBadRequest
from django.utils.translation import ugettext as _
from django.views import generic

from .. import forms
from backend.base.models import LogEntry


class UserLogEntriesView(LoginRequiredMixin, generic.ListView):

    """List all log entries of an user

    - In order to allow creation of any kind of logo entry, a special
      engineering on forms was required: we push all possible forms into the
      template context to later process input with the according model form.
    """

    page_title = _('My log')
    template_name = 'log/log_list.jade'

    def get_queryset(self):
        return LogEntry.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        data = super(UserLogEntriesView, self).get_context_data(**kwargs)

        # Include the possible log entry forms
        data['creation_forms'] = [
            forms.log.SMSEntryForm(),
        ]

        return data


class UserLogEntryCreate(LoginRequiredMixin, generic.CreateView):

    """Create a log entry of specific type

    - In order to allow creation of any kind of logo entry, a special
      engineering on forms was required: we retrieve the form class according
      to the requested log entry type, which should be specified by POST.
    """

    page_title = _('Create log entry')
    template_name = 'log/entry_create.jade'

    _form_class_map = {
        'sms': forms.log.SMSEntryForm,
    }

    def get_form_class(self):
        # Retrieve form class according to requested type
        return self._form_class_map[self.kwargs['type']]

    def form_valid(self, form):
        # Assign the user to the newly created log entry
        entry = form.save(commit=False)
        entry.user = self.request.user
        entry.save()

        # Message the user
        messages.success(self.request, _(
            '{} created successfuly.'
            .format(form.model_verbose_name)))

        return super(UserLogEntryCreate, self).form_valid(form)

    def get_success_url(self):
        return r('log:log')
