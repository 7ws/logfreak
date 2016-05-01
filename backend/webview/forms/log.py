from django import forms

from backend.sms_logger.models import SMSEntry


class BaseLogEntryForm(forms.ModelForm):

    """Abstract model form providing base functionality
    """

    @property
    def model_type(self):
        return self._meta.model._entry_type

    @property
    def model_verbose_name(self):
        return self._meta.model._meta.verbose_name


class SMSEntryForm(BaseLogEntryForm):

    """Simple form to insert a new bare LogEntry
    """

    class Meta:
        model = SMSEntry
        fields = ('contact_phone', 'text', 'datetime', 'received',)
