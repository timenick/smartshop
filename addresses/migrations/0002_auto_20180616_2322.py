# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-16 15:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
