# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-25 12:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('labels', '0001_initial'),
        ('racks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='rackID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='racks.Rack'),
        ),
    ]
