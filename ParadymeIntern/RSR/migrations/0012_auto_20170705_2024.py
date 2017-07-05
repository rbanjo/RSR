# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-05 20:24
from __future__ import unicode_literals

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('RSR', '0011_auto_20170705_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='language',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('English', 'English'), ('Spanish', 'Spanish'), ('French', 'French'), ('Chinese', 'Chinese')], max_length=30),
        ),
    ]
