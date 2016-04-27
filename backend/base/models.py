from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class BaseModel(models.Model):

    """An abstract model that provides basic functionality
    """

    # Owner
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        related_name='%(app_label)s_%(class)s_set',
    )

    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LogEntry(BaseModel):

    """Representation of a log entry

    This model is the base for any kind of log entry.
    """

    contact = models.ForeignKey(
        'base.Contact',
        editable=False,
        null=True,
    )


class Contact(BaseModel):

    """Representation of the contact related to a log entry

    A contact might represent a person or a "thing" (e.g. an organisation).
    """

    TYPE_PERSON = 'p'
    TYPE_THING = 't'

    type = models.CharField(
        choices=[
            (TYPE_PERSON, 'Person'),
            (TYPE_THING, 'Thing'),
        ],
        max_length=1,
    )

    name = models.CharField(
        max_length=100,
    )


class ContactPhone(BaseModel):

    """Representation of the phone number of a contact
    """

    contact = models.ForeignKey(
        'base.Contact',
    )
    msisdn = models.CharField(
        max_length=15,  # Max MSISDN length recommended by ITU-T - E.164
        validators=[
            RegexValidator(r'^\d+$'),  # Only digits are accepted
        ],
    )
    label = models.CharField(
        blank=True,
        max_length=20,
        null=True,
    )

    class Meta:
        unique_together = ('contact', 'msisdn',)
