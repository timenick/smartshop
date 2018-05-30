# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-25 12:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('merchandises', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('EPC', models.CharField(max_length=20)),
                ('TID', models.CharField(blank=True, max_length=20)),
                ('status', models.IntegerField(default=0)),
                ('merchandiseID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='merchandises.Merchandise')),
            ],
        ),
    ]