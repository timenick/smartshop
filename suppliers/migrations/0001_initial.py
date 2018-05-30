# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-25 12:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('companyName', models.CharField(max_length=30)),
                ('contactName', models.CharField(max_length=20)),
                ('contactPhone', models.DecimalField(decimal_places=0, max_digits=11)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=20)),
                ('province', models.CharField(blank=True, max_length=20)),
                ('country', models.CharField(blank=True, max_length=20)),
                ('area', models.CharField(blank=True, max_length=15)),
                ('ability', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='categories.Category')),
            ],
            options={
                'ordering': ('companyName',),
            },
        ),
    ]