# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 02:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_verbosity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='type',
            new_name='_type',
        ),
    ]
