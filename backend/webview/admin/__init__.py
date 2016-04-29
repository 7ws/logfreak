from django.contrib import admin

from .base import ContactAdmin, ContactPhoneAdmin
from .sms_logger import SMSEntryAdmin
from backend.base.models import Contact, ContactPhone
from backend.sms_logger.models import SMSEntry


# Register for `base`
admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactPhone, ContactPhoneAdmin)

# Register for `sms_logger`
admin.site.register(SMSEntry, SMSEntryAdmin)
