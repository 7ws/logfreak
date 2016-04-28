from django.contrib import admin

from .models import Contact, ContactPhone


class BaseModelAdmin(admin.ModelAdmin):

    """Admin layer to fulfill every ModelAdmin for a BaseModel child

    This will provide functionality required for the built-in fields defined
    into BaseModel.
    """

    def save_model(self, request, obj, *args):
        # Save the logged user into the object
        if not hasattr(obj, 'user'):
            obj.user = request.user

        super(BaseModelAdmin, self).save_model(request, obj, *args)


class ContactAdmin(BaseModelAdmin):

    list_display = ('name', 'type', 'created',)


class ContactPhoneAdmin(BaseModelAdmin):

    list_display = ('msisdn', 'contact',)


admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactPhone, ContactPhoneAdmin)
