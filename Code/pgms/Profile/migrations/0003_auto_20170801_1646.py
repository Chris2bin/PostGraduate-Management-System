# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 08:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0002_auto_20170801_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='br_title',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Research Title'),
        ),
    ]
