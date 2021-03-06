# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-25 12:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shops', '0001_initial'),
        ('merchandises', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('number', models.IntegerField(default=1)),
                ('arriveDate', models.DateField()),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('merchandiseID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='merchandises.Merchandise')),
                ('shopID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shops.Shop')),
            ],
            options={
                'ordering': ('createTime',),
            },
        ),
    ]
