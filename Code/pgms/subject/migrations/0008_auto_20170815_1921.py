# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-15 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0007_auto_20170815_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='gpa',
            field=models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=3),
        ),
    ]
