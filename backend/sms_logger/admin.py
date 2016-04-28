from django.contrib import admin

from backend.base.admin import BaseModelAdmin
from .models import SMSEntry


class SMSEntryAdmin(BaseModelAdmin):

    list_display = ('contact_phone', 'type', 'datetime', 'text',)


admin.site.register(SMSEntry, SMSEntryAdmin)
