from django.db import models


class BaseModel(models.Model):

    """An abstract model that provides basic functionality
    """

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
