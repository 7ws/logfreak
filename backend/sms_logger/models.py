from django.db import models
from django.utils.translation import ugettext as _

from backend.base.models import LogEntry


class SMSEntry(LogEntry):

    """Representation of a SMS log entry
    """

    TYPE_INCOMING = 'i'
    TYPE_OUTCOMING = 'o'

    type = models.CharField(
        choices=[
            (TYPE_INCOMING, _('Incoming')),
            (TYPE_OUTCOMING, _('Outcoming')),
        ],
        max_length=1,
    )
    contact_phone = models.ForeignKey(
        'base.ContactPhone',
        help_text=_('The phone number related to the contact.'),
        verbose_name=_('contact phone'),
    )
    text = models.TextField(
        help_text=_('The SMS\' full text.'),
        verbose_name=_('SMS text'),
    )
    received = models.BooleanField(
        help_text=_(
            'A flag indicating whether an outcoming SMS was received.'),
        verbose_name=_('received'),
    )
    datetime = models.DateTimeField(
        verbose_name=_('date and time'),
        help_text=_('Date and time the SMS was sent/received.'),
    )

    class Meta:
        verbose_name = _('SMS message')
        verbose_name_plural = _('SMS messages')

    def __str__(self):
        return 'SMS {preposition} {contact}'.format(
            preposition=(
                'from' if self.type == SMSEntry.TYPE_INCOMING else 'to'),
            contact=self.contact,
        )
