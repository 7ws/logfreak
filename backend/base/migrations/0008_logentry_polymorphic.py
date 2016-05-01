# -*- coding: utf-8 -*-
# Partially enerated by Django 1.9.5 on 2016-05-01 06:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def forwards_func(apps, schema_editor):
    """Populate `polymorphic_ctype` on the affected models
    """
    SMSEntry = apps.get_model('sms_logger', 'SMSEntry')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    ct = ContentType.objects.get_for_model(SMSEntry)
    SMSEntry.objects.all().update(polymorphic_ctype=ct)


def backwards_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('base', '0007_msisdn_minlength'),
        ('sms_logger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_base.logentry_set+', to='contenttypes.ContentType'),
        ),
        migrations.RunPython(forwards_func, backwards_func),
    ]
