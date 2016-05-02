from .base import BaseModelAdmin


class SMSEntryAdmin(BaseModelAdmin):

    list_display = ('contact_phone', '_type', 'datetime', 'text',)
