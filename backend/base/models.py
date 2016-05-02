from django.conf import settings
from django.core import validators
from django.db import models
from django.utils.translation import ugettext as _
from polymorphic.models import PolymorphicModel


class BaseModel(models.Model):

    """An abstract model that provides basic functionality
    """

    # Owner
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        related_name='%(app_label)s_%(class)s_set',
        verbose_name=_('owner'),
    )

    # Timestamps
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('creation timestamp')
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_('update timestamp')
    )

    class Meta:
        abstract = True


class LogEntry(PolymorphicModel, BaseModel):

    """Representation of a log entry

    This model is the base for any kind of log entry.
    """

    contact = models.ForeignKey(
        'base.Contact',
        editable=False,
        null=True,
        verbose_name=_('related contact'),
    )
    source = models.ForeignKey(
        'base.Source',
        editable=False,
        null=True,
        verbose_name=_('related source'),
    )


class Source(PolymorphicModel, BaseModel):

    """A configured source for retrieving log entries
    """

    # OAuth fields
    access_token = models.TextField(
        editable=False,
        null=True,  # Not every source needs it
    )
    access_token_secret = models.TextField(
        editable=False,
        null=True,  # Not every source needs it
    )


class Contact(BaseModel):

    """Representation of the contact related to a log entry

    A contact might represent a person or a "thing" (e.g. an organisation).
    """

    TYPE_PERSON = 'p'
    TYPE_THING = 't'

    _type = models.CharField(
        choices=[
            (TYPE_PERSON, 'Person'),
            (TYPE_THING, 'Thing'),
        ],
        help_text=_(
            'The type of contact; either a person or a thing (e.g. company).'),
        max_length=1,
        verbose_name=_('type'),
    )

    name = models.CharField(
        help_text=_('The name of the contact. Try to avoid repeatable names.'),
        max_length=100,
        verbose_name=_('name'),
    )

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')

    def __str__(self):
        return self.name


class ContactPhone(BaseModel):

    """Representation of the phone number of a contact
    """

    contact = models.ForeignKey(
        'base.Contact',
        help_text=_('The contact that owns this phone number.'),
        verbose_name=_('phone owner'),
    )
    msisdn = models.CharField(
        help_text=_('The phone number, including country code. Digits only.'),
        max_length=15,  # Max MSISDN length recommended by ITU-T - E.164
        validators=[
            validators.MinLengthValidator(9),
            validators.RegexValidator(r'^\d+$'),  # Only digits are accepted
        ],
        verbose_name=_('MSISDN (number)'),
    )
    label = models.CharField(
        blank=True,
        help_text=_('An optional label to represent this phone number.'),
        max_length=20,
        null=True,
        verbose_name=_('label'),
    )

    class Meta:
        unique_together = ('contact', 'msisdn',)
        verbose_name = _('contact phone')
        verbose_name_plural = _('contact phones')

    def __str__(self):
        if self.label:
            text = '{msisdn} ({label}) - {contact.name}'
        else:
            text = '{msisdn} - {contact.name}'
        return text.format(
            msisdn=self.msisdn,  # TODO: Add some formatting
            label=self.label,
            contact=self.contact,
        )
