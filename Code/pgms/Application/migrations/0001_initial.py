# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-19 11:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name_first', models.CharField(max_length=250)),
                ('app_name_last', models.CharField(max_length=250, null=True)),
                ('app_birthday', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('app_gender', models.CharField(choices=[('Female', 'Female'), ('Male', 'Male')], max_length=6)),
                ('app_ic', models.CharField(max_length=12)),
                ('app_nation', models.CharField(max_length=20, null=True)),
                ('app_address', models.TextField(max_length=100, null=True)),
                ('app_email', models.EmailField(max_length=100)),
                ('app_file_upload', models.FileField(null=True, upload_to='File/', verbose_name='Document')),
                ('app_file_upload2', models.ImageField(null=True, upload_to='File/', verbose_name='Photo')),
                ('app_mobile_number', models.CharField(max_length=20, null=True)),
                ('app_type', models.CharField(choices=[('By Research', 'By Research'), ('By Coursework', 'By Coursework')], max_length=13, null=True)),
                ('app_programme', models.CharField(max_length=100, null=True)),
                ('app_payment_status', models.CharField(choices=[('Paid', 'Paid'), ('Not Paid', 'Not Paid')], max_length=10, null=True)),
                ('app_file_upload3', models.FileField(null=True, upload_to='File/', verbose_name='Qualification')),
                ('app_created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('app_updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('app_admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL, verbose_name='Approving Admin')),
                ('app_student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
        ),
    ]
