# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2020-09-01 10:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0011_auto_20200401_0241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='others_order',
            name='estate',
            field=models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='no', max_length=10),
        ),
    ]
