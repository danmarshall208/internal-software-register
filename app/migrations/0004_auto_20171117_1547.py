# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-17 04:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_feedback_sesa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tool',
            name='created_by',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tool',
            name='developer',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tool',
            name='short_description',
            field=models.CharField(max_length=500),
        ),
    ]