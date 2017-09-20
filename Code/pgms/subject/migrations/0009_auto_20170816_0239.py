# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-15 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0008_auto_20170815_1921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='gpa',
        ),
        migrations.AddField(
            model_name='enroll',
            name='gpa',
            field=models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=3),
        ),
    ]
